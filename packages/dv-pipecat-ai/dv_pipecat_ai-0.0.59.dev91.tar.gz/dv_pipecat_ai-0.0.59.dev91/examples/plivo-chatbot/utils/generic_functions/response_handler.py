"""Response formatters for API responses.

This module contains formatter functions that process API responses
before they are returned to the LLM, allowing for custom formatting
and data transformation.
"""

import pandas as pd
from loguru import logger

# Dictionary to store all registered response formatters
response_formatters = {}


def register_response_formatter(name):
    """Decorator to register a response formatter function."""

    def decorator(func):
        response_formatters[name] = func
        return func

    return decorator


# Example response formatter
@register_response_formatter("practo_slots_formatter")
async def practo_slots_formatter(response_data, args):
    """Process order details response."""
    logger.debug(
        f"Processing order details response for doctor: {args.get('doctor_id', 'unknown')}"
    )
    logger.debug(f"Response: {response_data}")

    slots_dict = response_data.get("slots", [])
    amount = response_data.get("amount", "Not Available")
    base_df = pd.DataFrame.from_records(slots_dict)
    base_df_processed_list = []

    for _, base_row in base_df.iterrows():
        slot_info = base_row.get("slots", [])
        slot_info_list = []
        row_dict = dict(base_row)
        row_dict.pop("slots", None)

        for slot_info_item in slot_info:
            slot_info_dict = {}

            for key, value in slot_info_item.items():
                if isinstance(value, list) and value:
                    for key_, value_ in value[0].items():
                        slot_info_dict[f"{key}_{key_}"] = value_
                else:
                    slot_info_dict[key] = value

            slot_info_list.append(slot_info_dict)

        slot_info_df = pd.DataFrame.from_records(slot_info_list)

        for key__, value__ in row_dict.items():
            if not isinstance(value__, list):
                slot_info_df[key__] = value__

        base_df_processed_list.append(slot_info_df)

    base_df_processed_df = pd.concat(base_df_processed_list, ignore_index=True)
    base_df_processed_df = base_df_processed_df.fillna({"banner_text": "", "relDay": ""})
    filtered_df = base_df_processed_df.query("available == True")

    if filtered_df.shape[0] > 0:
        date_filter = sorted(filtered_df.datestamp.unique())[:3]
        filtered_df = filtered_df[filtered_df.datestamp.isin(date_filter)]
        filtered_df["hour"] = filtered_df["ts"].astype("datetime64[ns]").dt.hour.astype(str) + ":00"
        filtered_df.drop(columns=["ts", "datestamp"], inplace=True)
        llm_df = filtered_df[["date", "hour", "day", "weekDay", "relDay"]].drop_duplicates()

        llm_df["consultation_fee"] = amount
        print(llm_df.to_markdown(index=False))
        return llm_df.to_markdown(index=False)
    else:
        return "No slots available"
