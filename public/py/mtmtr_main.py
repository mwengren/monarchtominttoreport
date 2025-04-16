from pyscript import display, when
from datetime import datetime

from js import Blob, File, document, window
# from js import console
from io import BytesIO
from pyodide.ffi.wrappers import add_event_listener

#import monarchtominttoreport
from monarchtominttoreport import convert_csv, write_mint_csv

global df

# processFile is based on: https://stackoverflow.com/questions/77117847/how-can-i-import-a-file-into-pyscript-and-then-analyze-the-file-using-pyscript
@when('change', '#upload')
async def processFile(*args):
    csv_file = document.getElementById('upload').files.item(0)

    array_buf = await csv_file.arrayBuffer() # Get arrayBuffer from file
    file_bytes = array_buf.to_bytes() # convert to raw bytes array 
    csv_file = BytesIO(file_bytes) # Wrap in Python BytesIO file-like object

    global df
    # do monarchtominttoreport stuff:
    # df = monarchtominttoreport.convert.convert_csv(csv_file, dump = False)
    #df = monarchtominttoreport.convert_csv(csv_file, dump = False)
    df = convert_csv(csv_file, dump=False)
    display(f"Completed.  CSV columns: {[col for col in df.columns]}")


# Download file (based on: https://pyscript.recipes/2023.05.1/basic/file-download/)
def downloadFile(*args):
    global df
    now = datetime.now()
    time_label = now.strftime("%Y%m%d%H%M%S")        

    # csv_out = df.write_csv(date_format=("%m/%d/%Y"))
    #csv_out = monarchtominttoreport.convert.write_mint_csv(df=df)
    csv_out = write_mint_csv(df=df)

    file = File.new([csv_out], f"transactions-mint-{time_label}.csv", {type: "application/text"})
    url = window.URL.createObjectURL(file)

    hidden_link = document.createElement("a")
    hidden_link.setAttribute("download", f"transactions-mint-{time_label}.csv")
    hidden_link.setAttribute("href", url)
    hidden_link.click()

add_event_listener(document.getElementById("download"), "click", downloadFile)

# Download file example #2 (from: https://stackoverflow.com/questions/64669355/how-to-copy-download-file-created-in-pyodide-in-browser)
# this works but changes the browser page to show the csv file:
# csv_out = df.write_csv(date_format=("%m/%d/%Y"))
# blob = Blob.new([csv_out], {type : 'application/text'})
# url = window.URL.createObjectURL(blob)
# window.location.assign(url)
