import pandas as pd
from faker import Faker
import random


fake = Faker('pt-BR')

def generate_mock_transactions_data(num_records: int) -> pd.DataFrame:
    data = []
    for _ in range(num_records):
        transaction = {
            "id": fake.unique.random_int(min=1, max=10000),
            "user_id": 1,
            "description": fake.sentence(nb_words=6),
            "amount": round(random.uniform(10.0, 1000.0), 2),
            "transaction_type": random.choice(['income', 'expense']),
            "category_id": fake.random_int(min=1, max=6),
            "date": fake.date_time_this_year(),
            "created_at": fake.date_time_this_year(),
            "updated_at": fake.date_time_this_year(),
        }
        data.append(transaction)
    
    df = pd.DataFrame(data)
    return df


def generate_mock_goals_data(num_records: int) -> pd.DataFrame:
    data = []
    for _ in range(num_records):
        target_amount = round(random.uniform(500.0, 5000.0), 2)
        current_amount = round(random.uniform(0.0, target_amount), 2)
        goal = {
            "id": fake.unique.random_int(min=1, max=1000),
            "user_id": 1,
            "name": fake.sentence(nb_words=3),
            "target_amount": target_amount,
            "current_amount": current_amount,
            "color": fake.hex_color(),
            "icon": fake.word(),
            "created_at": fake.date_time_this_year(),
            "updated_at": fake.date_time_this_year(),
        }
        data.append(goal)
    
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    transactions_df = generate_mock_transactions_data(4000)
    goals_df = generate_mock_goals_data(20)
    
    print("Mock Transactions Data:")
    print(transactions_df.head())
    
    print("\nMock Goals Data:")
    print(goals_df.head())
    
    # 👇 ADICIONE ESSAS LINHAS 👇
    print("\nSalvando arquivos CSV...")
    
    transactions_df.to_csv(
        'transactions_mock.csv',  # Nome do arquivo
        index=False,              # Não salva o índice do pandas
        encoding='utf-8-sig'      # Garante acentuação correta
    )
    
    goals_df.to_csv(
        'goals_mock.csv',         # Nome do arquivo
        index=False,              
        encoding='utf-8-sig'
    )
    
    print("✅ Arquivos 'transactions_mock.csv' e 'goals_mock.csv' salvos!")