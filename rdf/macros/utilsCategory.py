
def plotCategory(key):
    plotCategoryDict = dict()
    plotCategoryDict.update({"kPlotData"      :[ 0]})
    plotCategoryDict.update({"kPlotqqWW"      :[ 1]})
    plotCategoryDict.update({"kPlotggWW"      :[ 2]})
    plotCategoryDict.update({"kPlotTop"       :[ 3]})
    plotCategoryDict.update({"kPlotDY"        :[ 4]})
    plotCategoryDict.update({"kPlotEWKSSWW"   :[ 5]})
    plotCategoryDict.update({"kPlotQCDSSWW"   :[ 6]})
    plotCategoryDict.update({"kPlotEWKWZ"     :[ 7]})
    plotCategoryDict.update({"kPlotWZ"        :[ 8]})
    plotCategoryDict.update({"kPlotZZ"        :[ 9]})
    plotCategoryDict.update({"kPlotNonPrompt" :[10]})
    plotCategoryDict.update({"kPlotVVV"       :[11]})
    plotCategoryDict.update({"kPlotTVX"       :[12]})
    plotCategoryDict.update({"kPlotVG"        :[13]})
    plotCategoryDict.update({"kPlotHiggs"     :[14]})
    plotCategoryDict.update({"kPlotDPSWW"     :[15]})
    plotCategoryDict.update({"kPlotWS"        :[16]})
    plotCategoryDict.update({"kPlotEM"        :[17]})
    plotCategoryDict.update({"kPlotOther"     :[18]})
    plotCategoryDict.update({"kPlotBSM"       :[19]})
    plotCategoryDict.update({"kPlotSignal0"   :[20]})
    plotCategoryDict.update({"kPlotSignal1"   :[21]})
    plotCategoryDict.update({"kPlotSignal2"   :[22]})
    plotCategoryDict.update({"kPlotSignal3"   :[23]})
    plotCategoryDict.update({"kPlotCategories":[24]})

    try:
        return plotCategoryDict[key][0]
    except Exception as e:
        print("Wrong key({0}): {1}".format(key,e))
