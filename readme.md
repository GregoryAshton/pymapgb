# pymapgb

This provides a `GBBasemap` for use in plotting geographic data for Great
Britain at the county level. We use data from the
[UK Data Service](http://census.edina.ac.uk/) to provide `Basemap` like object
in `matplotlib`.

## Motivation

I could not find a python module to plot maps of the UK with county level data.
If you know of any, please do let me know :D

## Installation

To install please run

    $ python setup.py install

This downloads all the shape-files and places them in `~/.shape_files` where
you can also add your own shape-files if you please. The module `pymapgb` 
should now be available to use.

## A simple example

A Minimum working example is provided in the file [`countries.py`](examples/countries.py), the
basics are as follows:

* First create a map instance:

    ```python
    import matplotlib.pyplot as plt
    from pymapgb import GBBasemap
    GBmap = GBBasemap()
    ```

* this provides several methods. The first is `draw_by_request`, this automates
alot of the work, for example to draw the outline of a country:

    ```python
    GBmap.draw_by_request("country", "england", facecolor="w", edgecolor="k")
    ```

* and to add county level data:

    ```python
    GBmap.draw_by_request("counties", "wales", colors='random')
    ```

* However what we want to draw is usually dictated by the data. To this end a
low level method is available `draw_by_file_name` which takes the file-name of
a shape-file (in the `~/.shape_files/` directory) and works directly from that.

<h3> Examples </h3>
<table width="200" height="400" cellspacing="0" border="0">

<tr>

<td align="center" valign="center">
    <a href="https://github.com/ga7g08/pymapgb">
    <figure>
    <img
    src="https://raw.githubusercontent.com/ga7g08/pymapgb/master/examples/countries.png"
    alt="" height="400" width="350">
    <figcaption> Countries of Great Britain
    </figure>
    </a>
<br />
</td>

<td align="center" valign="center">
    <a href="https://github.com/ga7g08/pymapgb">
    <figure>
    <img
    src="https://raw.githubusercontent.com/ga7g08/pymapgb/master/examples/counties.png"
    alt="" height="500" width="350">
    <figcaption> Counties of Great Britain 
    </figure>
    </a>
<br />
</td>

</tr>
</table>



## Status

This is in an early development status and requires quite a lot of work before
it can be useful generally. I would love it if you want to be involved, feel
free to PR anytime with anything you like. 

## TODO

* Fix missing English counties
* Documentation
* Implementation of coloring



