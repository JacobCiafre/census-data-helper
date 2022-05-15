from census_api import Search_Census, Get_Options
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    try:

        # getting data from api
        # print(Get_Options(2010)[2010]["cps/tobacco/aug"]) # quick way to check variables, change json to html to get human readable doc

        filename = "2010tobacco"
        filt = {"PEA3": "Frequency of smoking phrased 'Now smoke: every day, some days, not at all.'",
                "GESTCEN": "Geography-census state code"}
        surv, stcode = filt.keys()
        Search_Census(2010, 'cps/tobacco/aug', surv,
                      stcode, file_name=filename)

        # data management
        df = pd.read_csv(f'./data/{filename}.csv')

        # filter out all of the data values making up less than 1%
        totalCol = df[surv].size
        dfcalcs = df.groupby(surv)[[surv, stcode]].filter(
            lambda x: len(x) / totalCol > 0.01)

        # 0 indexing
        dfcalcs[surv] = dfcalcs[surv].replace(-1, 0)

        # plotting
        dfcalcs.plot(x=stcode, y=surv, kind='hexbin',
                     title="2010 Smoker Data", gridsize=7, cmap="RdPu", xlabel=filt[stcode], ylabel=filt[surv])

        plt.show()

    except AssertionError as err:
        print(f"{type(err).__name__}: {err}")
    except ValueError as err:
        print(f"{type(err).__name__}: {err}")
    except MemoryError as err:
        print(f"{type(err).__name__}: {err}")
    except ConnectionError as err:
        print(f"{type(err).__name__}: {err}")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
