# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long


from typing import Optional, List
import logging
import re
import requests
from ipulse_shared_base_ftredge import LogLevel,Action,  ProgressStatus, log_by_lvl,StructLog, DataResource

from ipulse_shared_data_eng_ftredge.pipelines import Pipelinemon, handle_pipeline_operation_exception, FunctionResult
import inspect

def source_eod_record_for_date_multiple_symbols_extended(api_token:str,
                                                  exchange_code_provider:str, 
                                                    records_origin_short_ref,
                                                    symbols:Optional[List[str]] = None,
                                                    date:Optional[str]=None,
                                                    pipelinemon:Optional[Pipelinemon]=None,
                                                    logger:Optional[logging.Logger]=None,
                                                    print_out:bool=False, raise_e:bool=False) -> FunctionResult:
    """
    THIS FUNCTION SHALL RETURN A LIST OF DICTS, WHERE EACH DICT REPRESENTS A RECORD.
    EODHD already send the data in this format.
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        api_url_without_token="",
        exchange_code_provider=exchange_code_provider,
        records_origin_short_ref=records_origin_short_ref
    )

    try:
        if records_origin_short_ref == "eodhd__eod_last_day_multiple_symbols":
            # Build API URL
            if symbols is None or len(symbols) == 0:
                api_url_without_token = (f"https://eodhd.com/api/eod-bulk-last-day/{exchange_code_provider}?fmt=json"
                    + (f"&date={date}" if date and len(date) == 10 else ""))

            else:
                api_url_without_token = (
                    f"https://eodhd.com/api/eod-bulk-last-day/{exchange_code_provider}?symbols={','.join(symbols)}&fmt=json"
                    + (f"&date={date}" if date and len(date) == 10 else "")
                )
            api_url_with_token = api_url_without_token + f"&api_token={api_token}"

            result.add_state("API Request Started")
            response = requests.get(url=api_url_with_token, timeout=30)
            result.add_state("Response Received")
            
            response.raise_for_status()
            result.data = response.json()
            result.add_metadata(
                api_url_without_token=api_url_without_token,
                total_records_fetched=len(result.data)
            )
            result.final()

            if pipelinemon:
                pipelinemon.add_log(StructLog(
                    level=LogLevel.INFO,
                    action=Action.READ_HTTP_GET,
                    source=DataResource.API_EXTERNAL,
                    destination=DataResource.IN_MEMORY_DATA,
                    progress_status=result.progress_status,
                    q=len(result.data),
                    description=result.get_final_report()
                ))

            log_by_lvl(
                info_msg=f"{function_name}: Fetched {len(result.data)} records",
                debug_msg=result.get_final_report(),
                logger=logger,
                print_out=print_out
            )
        else:
            raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_HTTP_GET,
            source=DataResource.API_EXTERNAL,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )

    return result



def source_eod_history_for_single_symbol_extended(
    api_token:str,
    asset_ref_at_provider:str,
    records_origin_short_ref:str, 
    from_date: Optional[str] = None, 
    to_date: Optional[str] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Fetch EOD history for a single symbol with optional date range.
    Returns a list of dicts, where each dict represents a record.
    
    Args:
        api_token (str): API authentication token
        asset_ref_at_provider (str): Asset reference/symbol
        records_origin_short_ref (str): Data provider reference
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        asset_ref_at_provider=asset_ref_at_provider,
        records_origin_short_ref=records_origin_short_ref,
        api_url_without_token=""
    )

    try:
        if records_origin_short_ref == "eodhd__eod_historic_bulk_single_symbol":
            # Build API URL
            api_url_without_token = f"https://eodhd.com/api/eod/{asset_ref_at_provider}?order=d&fmt=json"
            
            if from_date:
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", from_date):
                    raise ValueError(f"Date {from_date} should be in the format YYYY-MM-DD")
                api_url_without_token += f"&from={from_date}"
            if to_date:
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", to_date):
                    raise ValueError(f"Date {to_date} should be in the format YYYY-MM-DD")
                api_url_without_token += f"&to={to_date}"

            api_url_with_token = f"{api_url_without_token}&api_token={api_token}"
            
            result.add_state("API Request Started")
            response = requests.get(url=api_url_with_token, timeout=30)
            result.add_state("Response Received")
            
            response.raise_for_status()
            result.data = response.json()
            result.add_metadata(
                api_url_without_token=api_url_without_token,
                total_records_fetched=len(result.data)
            )
            result.final()

            if pipelinemon:
                pipelinemon.add_log(StructLog(
                    level=LogLevel.INFO,
                    action=Action.READ_HTTP_GET,
                    source=DataResource.API_EXTERNAL,
                    destination=DataResource.IN_MEMORY_DATA,
                    progress_status=result.progress_status,
                    q=len(result.data),
                    description=result.get_final_report()
                ))

            log_by_lvl(
                info_msg=f"{function_name}: Fetched {len(result.data)} records",
                debug_msg=result.get_final_report(),
                logger=logger,
                print_out=print_out
            )
        else:
            raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_HTTP_GET,
            source=DataResource.API_EXTERNAL,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )

    return result


#######################################################################################################################
#######################################################################################################################

