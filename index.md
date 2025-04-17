---
layout: default
title: Home
---


The monarchtominttoreport package (https://pypi.org/project/monarchtominttoreport) does the simple task of converting a transactions file output from the [Monarch Money accounting app](https://www.monarchmoney.com/) to the format used by the former Mint app. The Mint format is used by the [MintToReport](https://minttoreport.com/) reporting tool, which is no longer actively supported or updated.


<script type="py">
    from pyscript import display
    from datetime import datetime
    now = datetime.now()
    display(now.strftime("%m/%d/%Y, %H:%M:%S"))
</script>

<div class="row overflow-hidden" id="content">
    <div class="col mh-100 float-left" id="main">
        <div id="fileinput"></div>
        <input type="file" name="upload" id="upload">
    </div>
    <!---->
    <div class="col mh-100 float-left" id="main">
        <button id="download">Click to Download</button>
    </div>
    
</div>
<!---->
<script type="py" src="{{ site.baseurl }}/public/py/mtmtr_main.py" config="{{ site.baseurl }}/public/py/pyscript.json"></script>
<!--
"packages": ["pandas", "pyscript", "monarchtominttoreport>=0.2a4"],
<script type="py" src="mtmtr_main.py" config="pyscript.toml"></script>
-->