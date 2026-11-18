"""Plot-category IDs shared by the analysis helpers."""

_PLOT_CATEGORIES = {'kPlotData': 0,
 'kPlotqqWW': 1,
 'kPlotggWW': 2,
 'kPlotTT': 3,
 'kPlotTW': 4,
 'kPlotDY': 5,
 'kPlotEWKSSWW': 6,
 'kPlotQCDSSWW': 7,
 'kPlotEWKWZ': 8,
 'kPlotWZ': 9,
 'kPlotZZ': 10,
 'kPlotNonPrompt': 11,
 'kPlotVVV': 12,
 'kPlotTVX': 13,
 'kPlotVG': 14,
 'kPlotHiggs': 15,
 'kPlotWS': 16,
 'kPlotOther': 17,
 'kPlotEM': 18,
 'kPlotBSM': 19,
 'kPlotSignal0': 20,
 'kPlotSignal1': 21,
 'kPlotSignal2': 22,
 'kPlotSignal3': 23,
 'kPlotSignal4': 24,
 'kPlotSignal5': 25,
 'kPlotCategories': 26}

def plotCategory(key):
    try:
        return _PLOT_CATEGORIES[key]
    except Exception as e:
        print("Wrong key({0}): {1}".format(key,e))
