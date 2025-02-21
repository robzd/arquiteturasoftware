from typing import List, Optional
from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from entidades.tarefa import Tarefa
from casos_uso.caso_uso_tarefa import TarefaRepositoryInterface

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./tarefa.db"  # Você pode mudar o caminho se desejar salvar em outro local

Base = declarative_base()

# Definição da tabela 'Tarefa' no banco de dados
class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(String, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String)
    completa = Column(Boolean, default=False)

# Criando a engine e a sessão do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando a tabela
Base.metadata.create_all(bind=engine)

class SQLiteTarefaRepository(TarefaRepositoryInterface):
    def __init__(self):
        self.db = SessionLocal()

    def listar(self) -> List[Tarefa]:
        tarefas_db = self.db.query(TarefaDB).all()
        return [Tarefa(id=t.id, titulo=t.titulo, descricao=t.descricao, completa=t.completa) for t in tarefas_db]

    def buscar_por_id(self, id: str) -> Optional[Tarefa]:
        tarefa_db = self.db.query(TarefaDB).filter(TarefaDB.id == id).first()
        if tarefa_db:
            return Tarefa(id=tarefa_db.id, titulo=tarefa_db.titulo, descricao=tarefa_db.descricao, completa=tarefa_db.completa)
        return None

    def salvar(self, tarefa: Tarefa) -> Tarefa:
        tarefa_db = TarefaDB(id=tarefa.id, titulo=tarefa.titulo, descricao=tarefa.descricao, completa=tarefa.completa)
        self.db.add(tarefa_db)
        self.db.commit()
        self.db.refresh(tarefa_db)
        return Tarefa(id=tarefa_db.id, titulo=tarefa_db.titulo, descricao=tarefa_db.descricao, completa=tarefa_db.completa)

    def remover(self, id: str) -> None:
        self.db.query(TarefaDB).filter(TarefaDB.id == id).delete()
        self.db.commit()
