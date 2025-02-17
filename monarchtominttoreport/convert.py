import argparse
import polars as pl


def main() -> None:
    """
    Command line interface
    """
    kwargs = {
        'description': 'Convert a Monarch transaction export CSV file to a Mint transaction log to open in MintToReport',
        'formatter_class': argparse.RawDescriptionHelpFormatter
    }
    parser = argparse.ArgumentParser(**kwargs)

    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Path to a Monarch export transaction CSV file to read.')

    parser.add_argument('-o', '--output', type=str, required=False, default='monarchtomint-output.csv',
                        help='Path to write out the converted Mint-formatted transaction CSV file.')

    args = parser.parse_args()

    convert(args.input, args.output)
    
    return None



def convert(input: str, output: str) -> pl.DataFrame:
    """
    :param input: _description_
    :type input: str
    :param output: _description_
    :type output: str
    :return: _description_
    :rtype: pl.DataFrame
    """
    
    
    df = pl.read_csv(input, try_parse_dates=True)
    print(df.head)
    
    df = df.with_columns(
        pl.col("Original Statement").alias("Original Description"),
        pl.col("Tags").alias("Labels"),
        pl.col("Account").alias("Account Name"),
        pl.when(pl.col("Amount") > 0)
            .then(pl.lit("credit"))
            .otherwise(pl.lit("debit"))
            .alias("Transaction Type"),
        Description=pl.col("Merchant"),
        Amount=abs(pl.col("Amount"))
        
    ) 
    
    df = df.drop("Original Statement").drop("Merchant")
    
    
    print(df.head)
    #df.select([pl.col('Col3'), pl.col('Col2'), pl.col('Col1)])
    df_export=df.select([
        pl.col("Date"),
        pl.col("Description"),
        pl.col("Original Description"), 
        pl.col("Amount"), 
        pl.col("Transaction Type"),
        pl.col("Category"),
        pl.col("Account Name"), 
        pl.col("Labels"), 
        pl.col("Notes")  
    ])
    df_export.write_csv(output, date_format=("%m/%d/%Y")) 
    
    return df_export

if __name__ == '__main__':
    main()    
    



#def _load_apache_logs(apache_logs_dir):
    """
    Parses apache logs.

    Parameters
    ----------
    apache_logs_dir: str
        dir with apache log files

    Returns
    -------
    polars.DataFrame
        parsed requests information
    """