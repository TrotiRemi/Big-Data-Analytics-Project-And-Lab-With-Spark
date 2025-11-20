"""
PHASE 1: Bitcoin Blockchain Parser
========================================

Ce script parse les fichiers blk*.dat (format binaire Bitcoin Core)
et extrait les transactions dans des tables Spark.

Structure:
1. Lire les fichiers blk*.dat
2. Décoder les transactions (adresses, montants, timestamps)
3. Créer un DataFrame Spark
4. Sauvegarder les résultats
"""

import os
import struct
import hashlib
from datetime import datetime
from typing import List, Dict, Tuple
import io

from bitcoin.core import *
from bitcoin.core.script import *
import bitcoin

# Configuration Bitcoin mainnet
bitcoin.SelectParams('mainnet')

print("=" * 70)
print("BITCOIN BLOCKCHAIN PARSER - PHASE 1")
print("=" * 70)


# ============================================================================
# ÉTAPE 1: Lire les fichiers blk*.dat
# ============================================================================

class BlockFileParser:
    """Parser les fichiers blk*.dat du Bitcoin Core"""
    
    # Magic bytes pour identifier les blocs (mainnet)
    MAGIC_BYTES = b'\xf9\xbe\xb4\xd9'
    
    def __init__(self, blocks_dir: str):
        """
        Initialiser le parser
        
        Args:
            blocks_dir: Chemin vers le répertoire contenant les blk*.dat
        """
        self.blocks_dir = blocks_dir
        self.transactions = []
        
    def find_block_files(self) -> List[str]:
        """Trouver tous les fichiers blk*.dat"""
        block_files = []
        for filename in sorted(os.listdir(self.blocks_dir)):
            if filename.startswith('blk') and filename.endswith('.dat'):
                full_path = os.path.join(self.blocks_dir, filename)
                block_files.append(full_path)
                print(f"✓ Trouvé: {filename}")
        return block_files
    
    def read_varint(self, data: io.BytesIO) -> int:
        """
        Lire un varint (variable-length integer) du format Bitcoin
        
        Format Bitcoin varint:
        - < 0xfd: 1 byte
        - 0xfd + 2 bytes: 2-byte value
        - 0xfe + 4 bytes: 4-byte value
        - 0xff + 8 bytes: 8-byte value
        """
        first_byte = data.read(1)
        if not first_byte:
            return 0
        
        value = first_byte[0]
        if value < 0xfd:
            return value
        elif value == 0xfd:
            return int.from_bytes(data.read(2), 'little')
        elif value == 0xfe:
            return int.from_bytes(data.read(4), 'little')
        elif value == 0xff:
            return int.from_bytes(data.read(8), 'little')
    
    def parse_script(self, script_bytes: bytes) -> str:
        """
        Parser un script Bitcoin et extraire les adresses
        
        Note: Simplifié - on extrait les adresses P2PKH et P2SH
        """
        try:
            script = CScript(script_bytes)
            return str(script)[:100]  
        except:
            return "unknown"
    
    def parse_block(self, block_data: bytes) -> Dict:
        """
        Parser un bloc Bitcoin et extraire les transactions
        
        Structure du bloc:
        - 4 bytes: version
        - 32 bytes: previous block hash
        - 32 bytes: merkle root
        - 4 bytes: timestamp
        - 4 bytes: difficulty bits
        - 4 bytes: nonce
        - varint: nombre de transactions
        - transactions...
        """
        stream = io.BytesIO(block_data)
        
        try:
            # Lire l'en-tête du bloc (80 bytes)
            version = int.from_bytes(stream.read(4), 'little')
            prev_block_hash = stream.read(32).hex()
            merkle_root = stream.read(32).hex()
            timestamp = int.from_bytes(stream.read(4), 'little')
            bits = int.from_bytes(stream.read(4), 'little')
            nonce = int.from_bytes(stream.read(4), 'little')
            
            # Nombre de transactions
            tx_count = self.read_varint(stream)
            
            block_info = {
                'version': version,
                'prev_block_hash': prev_block_hash,
                'merkle_root': merkle_root,
                'timestamp': timestamp,
                'timestamp_readable': datetime.utcfromtimestamp(timestamp).isoformat(),
                'bits': bits,
                'nonce': nonce,
                'tx_count': tx_count,
                'transactions': []
            }
            
            # Parser chaque transaction
            for tx_idx in range(tx_count):
                tx_data = self.parse_transaction(stream, timestamp)
                if tx_data:
                    block_info['transactions'].append(tx_data)
            
            return block_info
        
        except Exception as e:
            print(f"✗ Erreur parsing bloc: {e}")
            return None
    
    def parse_transaction(self, stream: io.BytesIO, block_timestamp: int) -> Dict:
        """
        Parser une transaction Bitcoin
        
        Structure transaction:
        - 4 bytes: version
        - varint: nombre d'inputs
        - inputs...
        - varint: nombre d'outputs
        - outputs...
        - 4 bytes: locktime
        """
        try:
            tx_start_pos = stream.tell()
            
            version = int.from_bytes(stream.read(4), 'little')
            
            # Nombre d'inputs
            input_count = self.read_varint(stream)
            inputs = []
            
            for _ in range(input_count):
                input_data = self.parse_input(stream)
                inputs.append(input_data)
            
            # Nombre d'outputs
            output_count = self.read_varint(stream)
            outputs = []
            total_output_value = 0
            
            for _ in range(output_count):
                output_data = self.parse_output(stream)
                outputs.append(output_data)
                total_output_value += output_data.get('value', 0)
            
            locktime = int.from_bytes(stream.read(4), 'little')
            
            tx_end_pos = stream.tell()
            tx_size = tx_end_pos - tx_start_pos
            
            # Calculer le tx hash (simplifié - on utilise juste un ID)
            tx_hash = hashlib.sha256(hashlib.sha256(
                stream.getvalue()[tx_start_pos:tx_end_pos]
            ).digest()).digest().hex()[:16]  # Simplifié
            
            transaction = {
                'tx_hash': tx_hash,
                'version': version,
                'input_count': input_count,
                'output_count': output_count,
                'total_output_value': total_output_value,
                'locktime': locktime,
                'tx_size': tx_size,
                'timestamp': block_timestamp,
                'timestamp_readable': datetime.utcfromtimestamp(block_timestamp).isoformat(),
                'inputs': inputs,
                'outputs': outputs
            }
            
            return transaction
        
        except Exception as e:
            print(f"✗ Erreur parsing transaction: {e}")
            return None
    
    def parse_input(self, stream: io.BytesIO) -> Dict:
        """Parser un input (dépense)"""
        try:
            # Previous transaction hash
            prev_tx_hash = stream.read(32).hex()
            # Previous output index
            prev_output_index = int.from_bytes(stream.read(4), 'little')
            # Script length et script
            script_len = self.read_varint(stream)
            script = stream.read(script_len)
            # Sequence
            sequence = int.from_bytes(stream.read(4), 'little')
            
            return {
                'prev_tx_hash': prev_tx_hash,
                'prev_output_index': prev_output_index,
                'script': self.parse_script(script),
                'sequence': sequence
            }
        except:
            return {'prev_tx_hash': 'error', 'prev_output_index': 0}
    
    def parse_output(self, stream: io.BytesIO) -> Dict:
        """Parser un output (réception)"""
        try:
            # Valeur en satoshis
            value = int.from_bytes(stream.read(8), 'little')
            # Script length et script
            script_len = self.read_varint(stream)
            script = stream.read(script_len)
            
            return {
                'value': value,
                'script': self.parse_script(script)
            }
        except:
            return {'value': 0, 'script': 'error'}
    
    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parser un fichier blk*.dat complet
        
        Format du fichier:
        [Magic Bytes (4)] [Block Size (4)] [Block Data] [Magic Bytes] [Block Size] ...
        """
        blocks = []
        print(f"\n📄 Parsing {os.path.basename(filepath)}...")
        
        try:
            with open(filepath, 'rb') as f:
                block_count = 0
                
                while True:
                    # Chercher les magic bytes
                    magic = f.read(4)
                    if not magic or magic != self.MAGIC_BYTES:
                        break
                    
                    # Lire la taille du bloc
                    size_bytes = f.read(4)
                    if not size_bytes:
                        break
                    
                    block_size = int.from_bytes(size_bytes, 'little')
                    
                    # Lire les données du bloc
                    block_data = f.read(block_size)
                    if len(block_data) != block_size:
                        break
                    
                    # Parser le bloc
                    block_info = self.parse_block(block_data)
                    if block_info:
                        blocks.append(block_info)
                        block_count += 1
                        
                        if block_count % 100 == 0:
                            print(f"  ✓ {block_count} blocs parsés... ({block_info['timestamp_readable']})")
                
                print(f"✓ Total: {block_count} blocs trouvés")
                return blocks
        
        except Exception as e:
            print(f"✗ Erreur lecture fichier: {e}")
            return []
    
    def parse_all_files(self) -> List[Dict]:
        """Parser tous les fichiers blk*.dat"""
        all_blocks = []
        block_files = self.find_block_files()
        
        print(f"\n{'=' * 70}")
        print(f"PARSING DES FICHIERS BLOCKCHAIN")
        print(f"{'=' * 70}")
        
        for filepath in block_files:
            blocks = self.parse_file(filepath)
            all_blocks.extend(blocks)
        
        return all_blocks
    
    def extract_transactions(self, blocks: List[Dict]) -> List[Dict]:
        """
        Extraire toutes les transactions des blocs
        et les aplatir en une liste simple
        """
        transactions = []
        
        print(f"\n{'=' * 70}")
        print(f"EXTRACTION DES TRANSACTIONS")
        print(f"{'=' * 70}")
        
        for block_idx, block in enumerate(blocks):
            for tx in block.get('transactions', []):
                # Aplatir les transactions
                flat_tx = {
                    'tx_hash': tx['tx_hash'],
                    'timestamp': tx['timestamp'],
                    'timestamp_readable': tx['timestamp_readable'],
                    'input_count': tx['input_count'],
                    'output_count': tx['output_count'],
                    'total_output_value': tx['total_output_value'],
                    'tx_size': tx['tx_size'],
                    'block_hash': block['merkle_root'][:16],
                    'block_timestamp': block['timestamp']
                }
                transactions.append(flat_tx)
            
            if (block_idx + 1) % 50 == 0:
                print(f"✓ {block_idx + 1}/{len(blocks)} blocs traités")
        
        print(f"\n✓ Total transactions extraites: {len(transactions)}")
        return transactions


# ============================================================================
# ÉTAPE 2: Créer un DataFrame Spark
# ============================================================================

def create_spark_dataframe(transactions: List[Dict]):
    """
    Convertir les transactions en DataFrame Spark
    
    Schema:
    - tx_hash: string (ID unique de la transaction)
    - timestamp: long (Unix timestamp)
    - timestamp_readable: string (Format ISO)
    - input_count: int (nombre d'inputs)
    - output_count: int (nombre d'outputs)
    - total_output_value: long (montant total en satoshis)
    - tx_size: int (taille en bytes)
    - block_hash: string (hash du bloc)
    """
    from pyspark.sql import SparkSession
    from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType
    import sys
    
    print(f"\n{'=' * 70}")
    print(f"CRÉATION DU DATAFRAME SPARK")
    print(f"{'=' * 70}")
    
    # FIX: Configurer Spark pour utiliser le bon Python (évite erreur "Python worker failed to connect back")
    python_path = sys.executable
    print(f"📍 Python executable: {python_path}")
    
    # Initialiser Spark
    spark = SparkSession.builder \
        .appName("BDA-BlockchainParser") \
        .config("spark.sql.session.timeZone", "UTC") \
        .config("spark.pyspark.python", python_path) \
        .config("spark.pyspark.driver.python", python_path) \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()
    
    # Définir le schéma
    schema = StructType([
        StructField("tx_hash", StringType(), True),
        StructField("timestamp", LongType(), True),
        StructField("timestamp_readable", StringType(), True),
        StructField("input_count", IntegerType(), True),
        StructField("output_count", IntegerType(), True),
        StructField("total_output_value", LongType(), True),
        StructField("tx_size", IntegerType(), True),
        StructField("block_hash", StringType(), True)
    ])
    
    # Créer le DataFrame
    df = spark.createDataFrame(transactions, schema=schema)
    
    print(f"\n✓ DataFrame créé!")
    print(f"  Nombre de transactions: {df.count()}")
    print(f"  Partitions: {df.rdd.getNumPartitions()}")
    print(f"\nSchema:")
    df.printSchema()
    
    print(f"\nAperçu des données:")
    df.show(5, truncate=False)
    
    return spark, df


# ============================================================================
# ÉTAPE 3: Sauvegarder les résultats
# ============================================================================

def save_transactions_data(df, output_dir: str):
    """
    Sauvegarder les transactions dans différents formats
    
    Formats:
    1. Parquet (optimisé pour Spark)
    2. CSV (lisible et portable)
    3. JSON (flexible)
    """
    import os
    
    print(f"\n{'=' * 70}")
    print(f"SAUVEGARDE DES DONNÉES")
    print(f"{'=' * 70}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Parquet (meilleur pour Spark)
    parquet_path = os.path.join(output_dir, "btc_transactions.parquet")
    print(f"\n💾 Sauvegarde en Parquet: {parquet_path}")
    df.coalesce(1).write.mode("overwrite").parquet(parquet_path)
    print(f"✓ Parquet sauvegardé")
    
    # 2. CSV (lisible)
    csv_path = os.path.join(output_dir, "btc_transactions.csv")
    print(f"\n💾 Sauvegarde en CSV: {csv_path}")
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(csv_path)
    print(f"✓ CSV sauvegardé")
    
    # 3. Stats de base
    stats_path = os.path.join(output_dir, "blockchain_stats.txt")
    print(f"\n📊 Génération des statistiques...")
    
    with open(stats_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("BLOCKCHAIN STATISTICS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Total transactions: {df.count()}\n")
        
        # Statistiques par colonne
        stats = df.describe().collect()
        for row in stats:
            f.write(f"\n{row}\n")
        
        # Plages de dates
        date_range = df.select("timestamp_readable").collect()
        if date_range:
            f.write(f"\nDate range:\n")
            f.write(f"  First: {df.orderBy('timestamp').first()['timestamp_readable']}\n")
            f.write(f"  Last: {df.orderBy('timestamp').tail(1)[-1]['timestamp_readable']}\n")
    
    print(f"✓ Stats sauvegardés: {stats_path}")
    
    return parquet_path, csv_path


# ============================================================================
# MAIN: Orchestrer le pipeline complet
# ============================================================================

def main():
    """Pipeline complet de parsing blockchain"""
    
    # Configuration
    BLOCKS_DIR = r"data/blocks"
    OUTPUT_DIR = r"data/blockchain_parsed"
    
    # Vérifier que le répertoire existe
    if not os.path.exists(BLOCKS_DIR):
        print(f"✗ Erreur: {BLOCKS_DIR} n'existe pas!")
        return
    
    print(f"\n🚀 DÉMARRAGE PIPELINE BLOCKCHAIN PARSING")
    print(f"   Répertoire source: {BLOCKS_DIR}")
    print(f"   Répertoire sortie: {OUTPUT_DIR}")
    
    # === ÉTAPE 1: Parser les fichiers ===
    parser = BlockFileParser(BLOCKS_DIR)
    blocks = parser.parse_all_files()
    
    if not blocks:
        print("✗ Aucun bloc parsé!")
        return
    
    # === ÉTAPE 2: Extraire les transactions ===
    transactions = parser.extract_transactions(blocks)
    
    # === ÉTAPE 3: Créer DataFrame Spark ===
    spark, df = create_spark_dataframe(transactions)
    
    # === ÉTAPE 4: Sauvegarder ===
    save_transactions_data(df, OUTPUT_DIR)
    
    print(f"\n{'=' * 70}")
    print(f"✅ PIPELINE COMPLÉTÉ AVEC SUCCÈS!")
    print(f"{'=' * 70}")
    
    return spark, df


if __name__ == "__main__":
    spark, df = main()
    print(f"\n💡 Variables disponibles:")
    print(f"   - spark: SparkSession")
    print(f"   - df: DataFrame avec les transactions")
