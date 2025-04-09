import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.temporals import *
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe


def time_stat(self, stat="mean", over="time", window = None):
    """Method to calculate a stat over all time steps"""
    # create cdo command and run it

    # check if window is an int
    if window is not None:
        if isinstance(window, int):

            ## check if over is time 
            if over != "time":
                raise ValueError("You cannot supply a window if you are not grouping over all time periods")

            cdo_command = f"-timsel{stat},{window}"
            self.cdo_command(cdo_command, ensemble=False)
            return None
        else:
            raise ValueError("Window must be an integer")
    



    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    if over == "time":
        cdo_command = f"-tim{stat}"
        self.cdo_command(cdo_command, ensemble=False)
        return None

    if stat not in ["mean", "sum", "min", "max", "range", "var", "cumsum", "std"]:
        raise ValueError(f"{stat} is not a valid CDO stat!")

    # some tidying of over
    if isinstance(over, str):
        over = [over]

    over = [x.lower() for x in over]
    over = ["month" if "mon" in x else x for x in over]
    over = ["year" if "yea" in x else x for x in over]
    over = ["season" if "sea" in x else x for x in over]

    for x in over:
        if x not in ["day", "month", "year", "season", "hour"]:
            raise ValueError(f"{x} is not a valid group!")

    #  grouping over season and day and month makes no sense

    if "season" in over and ("month" in over or "day" in over):
        raise ValueError("You cannot group over season and day or month")

    over = sorted(list(set(over)))

    if over == ["day", "month"]:
        over = ["day"]

    if over == ["day", "hour", "month"]:
        over = ["day", "hour"]

    if over == ["day", "hour", "month", "year"]:
        over = ["day", "hour", "year"]
    # sort over alphabetically

    run = False

    # single variables
    # daily climatology
    if over == ["day"]:
        run = True
        ydaystat(self, stat=stat)
        return None

    if over == ["day", "hour"]:
        run = True
        yhourstat(self, stat=stat)
        return None

    if over == ["day", "hour", "year"]:
        run = True
        hourstat(self, stat=stat)
        return None

    if over == ["hour"]:
        run = True
        dhourstat(self, stat=stat)
        return None

    # monthly climatology
    if over == ["month"]:
        run = True
        ymonstat(self, stat=stat)
        return None

    # annual mean
    if over == ["year"]:
        run = True
        yearlystat(self, stat=stat)
        return None

    # seasonal climatology
    if over == ["season"]:
        run = True
        seasclim(self, stat=stat)
        return None

    # seasonal climatology
    if over == ["season", "year"]:
        run = True
        seasstat(self, stat=stat)
        return None

    # all three. This is daily mean

    if over == ["day", "month", "year"] or over == ["day", "year"]:
        run = True
        dailystat(self, stat=stat)
        return None

    # monthly mean

    if over == ["month", "year"]:
        run = True
        monstat(self, stat=stat)
        return None
    if run is False:
        raise ValueError(f"Grouping {over} is currently not supported!")


def tsum(self, over="time", align="right", window = None):
    """
    tsum: Calculate the temporal sum of all variables.

    Parameters
    -------------
    align : str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    over : str or list
        Time periods to count the sum over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R,
        so you can supply combinations of these to get the sum over each year, month or day.
    window : int
        This determines the number of time steps to sum over, on a non-rolling basis. 
        This is useful if you need to calculate the sum every 5 days, for example.

    Examples
    ------------
    If you want to calculate sum over all time steps. Do the following:
    >>> ds.tsum()
    If you want to calculate the sum over each year:
    >>> ds.tsum(over="year")
    If you want to calculate the sum over each month. This will add up all data in each month across all years not within each year.
    >>> ds.tsum(over="month")
    If you want to calculate the sum over each day. This will add up all data in each day across all years not within each year.
    >>> ds.tsum(over="day")

    """
    self.align(align)
    time_stat(self, stat="sum", over=over, window = window)


def na_count(self, over="time", align="right", window = None):
    """
    na_count: Calculate the number of missing values.

    Parameters
    -------------
    over: str or list
        Time periods to to the count over over. Options are 'time', 'year', 'month', 'day'.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window : int
        This determines the number of time steps to calculate, on a non-rolling basis. 
        This is useful if you need to calculate the sum every 5 days, for example.

    Examples
    ------------
    If you want to calculate the number of missing values over all time steps. Do the following:
    >>> ds.na_count()
    If you want to calculate the number of missing values in each year:
    >>> ds.na_count(over="year")
    """
    self.align(align)

    self.run()

    for vv in self.variables:
        self.cdo_command(f"-aexpr,'{vv}=isMissval({vv})'")

    self.tsum(over=over, window = window)


def na_frac(self, over="time", align="right", window = None):
    """
    na_frac: Calculate the fraction of missing values in each grid cell across all time steps.

    Parameters
    -------------
    over: str or list
        Time periods to to the count over over. Options are 'time', 'year', 'month', 'day'.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window: int
        This determines the number of time steps to calculate over, on a non-rolling basis. 
        This is useful if you need to calculate the fraction for every non-overlapping 5 day periods, for example.

    Examples
    ------------
    If you want to calculate the fraction of missing values over all time steps. Do the following:
    >>> ds.na_frac()
    If you want to calculate the fraction of missing values in each year:
    >>> ds.na_frac(over="year")

    """
    self.align(align)

    self.run()

    for vv in self.variables:
        self.cdo_command(f"-aexpr,'{vv}=isMissval({vv})'")

    self.tmean(over=over, window = window)


def tmean(self, over="time", align="right", window = None):
    """
    tmean: Calculate the temporal mean of all variables.

    Useful for: monthly mean, annual/yearly mean, seasonal mean, daily mean, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window: int
        This determines the number of time steps to calculate the mean over to calculate over, on a non-rolling basis. 
        This is useful if you need to calculate the mean every 5 days, for example.

    Examples
    ------------
    If you want to calculate mean over all time steps. Do the following:

        >>> ds.tmean()

    If you want to calculate the mean for each year in a dataset, do this:

        >>> ds.tmean("year")

    If you want to calculate the mean for each month in each year in a dataset, do this:

        >>> ds.tmean(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological mean, you would do this:

        >>> ds.tmean( "month")

    A daily climatological mean would be the following:

        >>> ds.tmean( "day")


    """
    self.align(align=align)
    time_stat(self, stat="mean", over=over, window = window)


def tmin(self, over="time", align="right", window = None):
    """
    tmin: Calculate the temporal minimum of all variables.

    Useful for: monthly minimum, annual/yearly minimum, seasonal minimum, daily minimum, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R, with over acting as the grouping.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window: int
        This determines the number of time steps to calculate the minimum over to calculate over, on a non-rolling basis. 
        This is useful if you need to calculate the minimum every 5 days, for example.

    Examples
    ------------
    If you want to calculate minimum over all time steps. Do the following:

        >>> ds.tmin()

    If you want to calculate the minimum for each year in a dataset, do this:

        >>> ds.tmin("year")

    If you want to calculate the minimum for each month in a dataset, do this:

        >>> ds.tmin("month")

    If you want to calculate the minimum for each month in each year in a dataset, do this:

        >>> ds.tmin(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological min, you would do this:

        >>> ds.tmin( "month")

    A daily climatological minimum would be the following:

        >>> ds.tmin( "day")

    """
    self.align(align=align)
    time_stat(self, stat="min", over=over, window = window)


def tmax(self, over="time", align="right", window = None):
    """
    tmax: Calculate the temporal maximum of all variables.

    Useful for: monthly maximum, annual/yearly maximum, seasonal maximum, daily maximum, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R, with over acting as the grouping.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window: int
        This determines the number of time steps to calculate the maximum over to calculate over, on a non-rolling basis. 
        This is useful if you need to calculate the maximum every 5 days, for example.

    Examples
    ------------
    If you want to calculate maximum over all time steps. Do the following:

        >>> ds.tmax()

    If you want to calculate the maximum for each year in a dataset, do this:

        >>> ds.tmax("year")

    If you want to calculate the maximum for each month in a dataset, do this:

        >>> ds.tmax("month")

    If you want to calculate the maximum for each month in each year in a dataset, do this:

        >>> ds.tmax(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological max, you would do this:

        >>> ds.tmax( "month")

    A daily climatological maximum would be the following:

        >>> ds.tmax( "day")
    """
    self.align(align=align)
    time_stat(self, stat="max", over=over, window = window)


def tmedian(self, over="time", align="right"):
    """
    tmedian: Calculate the temporal median of all variables.

    Useful for: monthly median, annual/yearly median, seasonal median, daily median, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R, with over acting as the grouping.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate median over all time steps. Do the following:

        >>> ds.tmedian()

    If you want to calculate the median for each year in a dataset, do this:

        >>> ds.tmedian("year")

    If you want to calculate the median for each month in a dataset, do this:

        >>> ds.tmedian("month")

    If you want to calculate the median for each month in each year in a dataset, do this:

        >>> ds.tmedian(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological median, you would do this:

        >>> ds.tmedian( "month")

    A daily climatological median would be the following:

        >>> ds.tmedian( "day")
    """
    self.align(align=align)
    self.tpercentile(p=50, over=over)


def trange(self, over="time", align="right", window = None):
    """
    trange: Calculate the temporal range of all variables
    Useful for: monthly range, annual/yearly range, seasonal range, daily range, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R, with over acting as the grouping.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window: int
        This determines the number of time steps to calculate the range over to calculate over, on a non-rolling basis. 
        This is useful if you need to calculate the range every 5 days, for example.

    Examples
    ------------
    If you want to calculate range over all time steps. Do the following:

        >>> ds.trange()

    If you want to calculate the range for each year in a dataset, do this:

        >>> ds.trange("year")

    If you want to calculate the range for each month in a dataset, do this:

        >>> ds.trange("month")

    If you want to calculate the range for each month in each year in a dataset, do this:

        >>> ds.trange(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological range, you would do this:

        >>> ds.trange( "month")

    A daily climatological range would be the following:

        >>> ds.trange( "day")

    """
    self.align(align=align)
    time_stat(self, stat="range", over=over, window = window)


def tvar(self, over="time", align="right", window = None):
    """
    tvar: Calculate the temporal variance of all variables
    Useful for: monthly variance, annual/yearly variance, seasonal variance, daily variance, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R, with over acting as the grouping.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window: int
        This determines the number of time steps to calculate the variance over to calculate over, on a non-rolling basis. 
        This is useful if you need to calculate the variance every 5 days, for example.

    Examples
    ------------
    If you want to calculate variance over all time steps. Do the following:

        >>> ds.tvar()

    If you want to calculate the variance for each year in a dataset, do this:

        >>> ds.tvar("year")

    If you want to calculate the variance for each month in a dataset, do this:

        >>> ds.tvar("month")

    If you want to calculate the variance for each month in each year in a dataset, do this:

        >>> ds.tvar(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological var, you would do this:

        >>> ds.tvar( "month")

    A daily climatological variance would be the following:

        >>> ds.tvar( "day")
    """
    self.align(align=align)
    time_stat(self, stat="var", over=over, window = window)


def tstdev(self, over="time", align="right", window = None):
    """
    tstdev: Calculate the temporal standard deviation of all variables
    Useful for: monthly standard deviation, annual/yearly standard deviation, seasonal standard deviation, daily standard deviation, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R, with over acting as the grouping.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    window: int
        This determines the number of time steps to calculate the standard deviation over to calculate over, on a non-rolling basis. 
        This is useful if you need to calculate the standard deviation every 5 days, for example.


    Examples
    ------------
    If you want to calculate standard deviation over all time steps. Do the following:

        >>> ds.tstdev()

    If you want to calculate the standard deviation for each year in a dataset, do this:

        >>> ds.tstdev("year")

    If you want to calculate the standard deviation for each month in a dataset, do this:

        >>> ds.tstdev("month")

    If you want to calculate the standard deviation for each month in each year in a dataset, do this:

        >>> ds.tstdev(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological var, you would do this:

        >>> ds.tstdev("month")

    A daily climatological standard deviation would be the following:

        >>> ds.tstdev("day")
    """
    self.align(align=align)
    time_stat(self, stat="std", over=over, window = window)


def tcumsum(self, align="right"):
    """
    tcumsum: Calculate the temporal cumulative sum of all variables

    Parameters
    -------------
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate the cumulative sum for all variables over all timesteps, do this:

        >>> ds.tcumsum()

    """
    self.align(align=align)
    # create cdo command and runit
    time_stat(self, stat="cumsum")


def tpercentile(self, p=None, over="time", align="right"):
    """
    tpercentile: Calculate the temporal percentile of all variables
    Useful for monthly percentile, annual/yearly percentile, seasonal percentile, daily percentile, daily climatology, monthly climatology, seasonal climatology

    Parameters
    -------------
    p: float or int
        Percentile to calculate
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
        This operates in a similar way to the groupby method in pandas or the tidyverse in R, with over acting as the grouping.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate the 20th percentile over all time steps. Do the following:

        >>> ds.tpercentile(20)

    If you want to calculate the 20th percentile for each year in a dataset, do this:

        >>> ds.tpercentile(20)

    If you want to calculate the 20th percentile for each year in a dataset, do this:

        >>> ds.tpercentile(p= 20, over = "year")

    """
    self.align(align=align)

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    over = over
    if p is None:
        raise ValueError("Please supply p")

    if not isinstance(p, (int, float)):
        raise TypeError("p is a " + str(type(p)) + ", not int or float")

    if (p < 0) or (p > 100):
        raise ValueError("p: " + str(p) + " is not between 0 and 100!")

    self.run()

    # create cdo command and run it

    if isinstance(over, str):
        over = [over]

    for x in over:
        if x not in ["day", "month", "year", "season", "time"]:
            raise ValueError(f"{x} is not a valid group!")

    #  grouping over season and day and month makes no sense

    if "season" in over and ("month" in over or "day" in over):
        raise ValueError("You cannot group over season and day or month")

    over = sorted(list(set(over)))

    if over == ["day", "month"]:
        over = ["day"]

    if over == ["time"]:
        perc_term = "cdo -timpctl,"
        min_command = " -timmin "
        max_command = " -timmax "

    # single variables
    # daily climatology
    if over == ["day"]:
        perc_term = "cdo -ydaypctl,"
        min_command = " -ydaymin "
        max_command = " -ydaymax "

    # monthly climatology
    if over == ["month"]:
        perc_term = "cdo -ymonpctl,"
        min_command = " -ymonmin "
        max_command = " -ymonmax "

    # annual mean
    if over == ["year"]:
        perc_term = "cdo -yearpctl,"
        min_command = " -yearmin "
        max_command = " -yearmax "

    # seasonal climatology
    if over == ["season"]:
        perc_term = "cdo -yseaspctl,"
        min_command = " -yseasmin "
        max_command = " -yseasmax "

    # seasonal climatology
    if over == ["season", "year"]:
        perc_term = "cdo -seaspctl,"
        min_command = " -seasmin "
        max_command = " -seasmax "

    # all three. This is daily mean

    if over == ["day", "month", "year"] or over == ["day", "year"]:
        perc_term = "cdo -daypctl,"
        min_command = " -daymin "
        max_command = " -daymax "

    # monthly mean

    if over == ["month", "year"]:
        perc_term = "cdo -monpctl,"
        min_command = " -monmin "
        max_command = " -monmax "

    new_files = []
    new_commands = []
    for ff in self:
        target = temp_file("nc")

        cdo_command = (
            perc_term
            # "cdo -timpctl,"
            + str(p)
            + " "
            + ff
            + min_command
            + ff
            + max_command
            + ff
            + " "
            + target
        )

        cdo_command = tidy_command(cdo_command)
        target = run_cdo(cdo_command, target, precision=self._precision)
        new_files.append(target)
        new_commands.append(cdo_command)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    cleanup()
