import json
from typing import List, Optional
from sqlalchemy.orm import Session
from etl.load import EdaTableModel
from app.schemas.stats import StatsIndexItem, StatsTableResponse

def get_stats_index(db: Session) -> List[StatsIndexItem]:
    tables = db.query(EdaTableModel).all()
    return [
        StatsIndexItem(
            table_name=t.table_name,
            insight=t.insight_sentence
        )
        for t in tables
    ]

def get_stats_table(db: Session, table_name: str) -> Optional[StatsTableResponse]:
    t = db.query(EdaTableModel).filter(EdaTableModel.table_name == table_name).first()
    if not t:
        return None
    data = json.loads(t.data_json)
    return StatsTableResponse(
        table_name=t.table_name,
        insight=t.insight_sentence,
        columns=data.get("columns", []),
        rows=data.get("rows", []),
    )
