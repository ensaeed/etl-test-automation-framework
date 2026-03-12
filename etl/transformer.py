import pandas as pd

POSTCODE_REGEX_STRICT_SPACE= r"^[A-Z]{1,2}\d[A-Z\d]?\s\d[A-Z]{2}$"

def transform_customers(df):
    out=df.copy()
    if "zipcode" in out.columns:
        out=out.rename(columns={"zipcode":"postcode"})

    out["postcode"]=out["postcode"].astype(str).str.strip().str.upper()
    out["created_at"]=pd.to_datetime(out["created_at"],errors="coerce")
    out["full_name"]=(out["first_name"].astype(str).str.strip()+" "+out["last_name"].astype(str).str.strip()).str.strip()
    postcode_ok=out["postcode"].str.match(POSTCODE_REGEX_STRICT_SPACE,case=False,na=False)
    created_ok=out["created_at"].notna()

    out["is_valid_record"]=postcode_ok & created_ok

    out=out.sort_values(["customer_id","created_at"],ascending=[True,False],na_position="last")
    out=out.drop_duplicates(subset=["customer_id"],keep="first").reset_index(drop=True)

    return out



