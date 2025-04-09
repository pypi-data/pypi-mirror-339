import inspect
import logging
from typing import Any, Dict, List, Optional, Union
from google.cloud import firestore
from ipulse_shared_base_ftredge import (
    LogLevel, DataResource, Action, ProgressStatus, StructLog
)
from ..pipelines import FunctionResult, Pipelinemon, handle_pipeline_operation_exception


def merge_firestore_document_extended(
    document_id: str,
    collection: str,
    data: Dict[str, Any],
    firestore_client: firestore.Client,
    merge: bool = True,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Write/update a Firestore document."""
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)

    try:
        doc_ref = firestore_client.collection(collection).document(document_id)
        doc_ref.set(data, merge=merge)
        
        result.add_metadata(document_id=document_id, collection=collection)
        result.add_state(f"Updated document {document_id} in collection {collection}")
        
        if pipelinemon:
            pipelinemon.add_system_impacted(f"firestore_write: {document_id}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=Action.PERSIST_MERGE_DOCUMENT,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.DB_FIRESTORE,
                progress_status=ProgressStatus.DONE,
                description=result.get_final_report()
            ))

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_MERGE_DOCUMENT,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.DB_FIRESTORE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result
