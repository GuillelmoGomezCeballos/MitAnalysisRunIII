"""Performance helpers used only by the independent optimized analysis macros.

This module does not initialize calibrations or change ROOT threading.
"""
import ROOT
from utilsCategory import plotCategory

def read_runs_metadata(df_runs):
    """Evaluate scalar metadata together, then all available replica sums.

    Two passes preserve the original indexed-column types, missing-column
    fallbacks and sample-wide minimum replica counts without repeated scans.
    """
    columns = {str(name) for name in df_runs.GetColumnNames()}
    scalars = {
        "sumw": df_runs.Sum("genEventSumw"),
        "events": df_runs.Sum("genEventCount"),
        "runs": df_runs.Count(),
    }
    for name in ("nLHEPdfSumw", "nLHEScaleSumw", "nPSSumw"):
        if name in columns:
            scalars[name] = df_runs.Min(name)
    values = {name: result.GetValue() for name, result in scalars.items()}
    replicas = [min(103, int(values["nLHEPdfSumw"])) if "nLHEPdfSumw" in values else 0, 9, 4]
    count = values["runs"]
    sums = [[count] * 9, [count] * 5]
    actions = []
    for output, size, count_name, vector_name, replica_index in (
        (0, 9, "nLHEScaleSumw", "LHEScaleSumw", 1),
        (1, 4, "nPSSumw", "PSSumw", 2),
    ):
        for index in range(size):
            if count_name not in values:
                replicas[replica_index] = index
            elif values[count_name] <= index:
                replicas[replica_index] = int(values[count_name])
            elif vector_name not in columns:
                replicas[replica_index] = index
            else:
                column = f"ssww_{vector_name}_{index}"
                df_runs = df_runs.Define(column, f"{vector_name}[{index}]")
                actions.append((output, index, df_runs.Sum(column)))
    for output, index, result in actions:
        sums[output][index] = result.GetValue()
    return values["sumw"], values["events"], replicas, sums[0], sums[1], count

def empty_histogram(template, name):
    histogram = template.Clone(name)
    histogram.SetDirectory(0)
    histogram.SetTitle(name)
    histogram.Reset()
    return histogram

ROOT.gInterpreter.Declare(r'''
#ifndef ANALYSIS_OPTIMIZED_HISTOGRAM_HELPERS
#define ANALYSIS_OPTIMIZED_HISTOGRAM_HELPERS
#include <TH1D.h>
#include <TH2D.h>
#include <cmath>
namespace optimized_histograms {
void fold_overflow(TH2D &h) {
    // Preserve the original ordering: y overflow first, then x overflow.
    for (int x = 1; x <= h.GetNbinsX(); ++x) {
        const int y = h.GetNbinsY();
        h.SetBinContent(x, y, h.GetBinContent(x, y) + h.GetBinContent(x, y + 1));
        h.SetBinError(x, y, std::sqrt(std::pow(h.GetBinError(x, y), 2) + std::pow(h.GetBinError(x, y + 1), 2)));
        h.SetBinContent(x, y + 1, 0.0);
        h.SetBinError(x, y + 1, 0.0);
    }
    for (int y = 1; y <= h.GetNbinsY(); ++y) {
        const int x = h.GetNbinsX();
        h.SetBinContent(x, y, h.GetBinContent(x, y) + h.GetBinContent(x + 1, y));
        h.SetBinError(x, y, std::sqrt(std::pow(h.GetBinError(x, y), 2) + std::pow(h.GetBinError(x + 1, y), 2)));
        h.SetBinContent(x + 1, y, 0.0);
        h.SetBinError(x + 1, y, 0.0);
    }
}
void add_y_bin(TH1D &target, const TH2D *source, int y) {
    for (int x = 1; x <= target.GetNbinsX(); ++x) {
        const double content = source ? source->GetBinContent(x, y) : 0.0;
        const double error = source ? source->GetBinError(x, y) : 0.0;
        target.SetBinContent(x, target.GetBinContent(x) + content);
        target.SetBinError(x, std::sqrt(std::pow(target.GetBinError(x), 2) + std::pow(error, 2)));
    }
}
}
#endif
''')


def candidate_categories(the_cat, include_nonprompt, include_wrong_charge=False):
    """Include SSWW charge migrations only when the analysis requests them."""
    categories = {the_cat}
    if include_nonprompt:
        categories.add(plotCategory("kPlotNonPrompt"))
    if include_wrong_charge:
        categories.add(plotCategory("kPlotWS"))
    return sorted(categories)


def histogram_value(result):
    return result.GetValue() if hasattr(result, "GetValue") else result


def materialize_empty_categories(histograms, active_categories, name_prefix="histo"):
    """Retain the original histogram schema without empty-category RDF actions."""
    for number, row in enumerate(histograms):
        result = next((row[x] for x in active_categories if row[x] != 0), None)
        if result is None:
            continue
        template = histogram_value(result)
        for category in range(len(row)):
            if row[category] == 0:
                row[category] = empty_histogram(template, f"{name_prefix}_{number}_{category}")


def project_ww_templates(histo2d, output, n_categories, mode, bins, low, high):
    """Preserve qqWW/ggWW generator decomposition and empty histogram entries."""
    if mode not in (1, 2):
        return
    for number, row in enumerate(histo2d):
        if not any(row):
            continue
        for category in range(n_categories):
            name = f"histoMVA_{number}_{category}"
            output[number][category] = ROOT.TH1D(name, name, bins, low, high)
            output[number][category].SetDirectory(0)
        for category in range(n_categories):
            source = histogram_value(row[category]) if row[category] != 0 else ROOT.nullptr
            if row[category] != 0:
                ROOT.optimized_histograms.fold_overflow(source)
            if category == plotCategory("kPlotqqWW"):
                targets = [plotCategory("kPlotqqWW")] + [plotCategory(f"kPlotSignal{i}") for i in range(3)]
            elif category == plotCategory("kPlotggWW"):
                targets = [plotCategory("kPlotqqWW")] + [plotCategory(f"kPlotSignal{i}") for i in range(3, 6)]
            else:
                targets = [category]
            for y_bin, target in enumerate(targets, 1):
                ROOT.optimized_histograms.add_y_bin(output[number][target], source, y_bin)


def project_wz_templates(histo2d, output, n_categories, n_histograms, x1_bins, x2_bins, split_qcd):
    """Preserve mode-7 WZ projection, including unused IDs and error resets."""
    # The legacy mode writes every ID 300..n_histograms-1, including gaps with
    # no TH2 action. Such gaps stay empty with zero entries.
    for number in range(300, n_histograms):
        bins = x1_bins if number < 500 else x2_bins
        for category in range(n_categories):
            name = f"histo_{number}_{category}"
            output[number][category] = ROOT.TH1D(name, name, len(bins)-1, bins)
            output[number][category].SetDirectory(0)
        row = histo2d[number]
        if not any(row):
            continue
        for category in range(n_categories):
            source = histogram_value(row[category]) if row[category] != 0 else ROOT.nullptr
            if row[category] != 0:
                ROOT.optimized_histograms.fold_overflow(source)
            if category == plotCategory("kPlotEWKWZ") or (category == plotCategory("kPlotWZ") and split_qcd):
                targets = [plotCategory("kPlotEWKWZ")] + [plotCategory(f"kPlotSignal{i}") for i in range(4)]
                for target in targets:
                    output[number][target].SetBinError(1, 0.0)
            else:
                targets = [category]
            for y_bin, target in enumerate(targets, 1):
                ROOT.optimized_histograms.add_y_bin(output[number][target], source, y_bin)


def project_ssww_templates(histo2d, histo_mva, n_categories, n_histograms, x1_bins, x2_bins, split_qcd=False):
    """Preserve every output category and the legacy projection/statistics order."""
    for number in range(n_histograms):
        # Every booked category has the same observable IDs. Omitted categories
        # are identically empty and need no RDF action or TH2 allocation.
        if not any(histo2d[number]):
            continue
        bins = x1_bins if number % 400 < 200 else x2_bins
        for category in range(n_categories):
            name = f"histoMVA_{number}_{category}"
            histo_mva[number][category] = ROOT.TH1D(name, name, len(bins) - 1, bins)
            histo_mva[number][category].SetDirectory(0)
        for category in range(n_categories):
            result = histo2d[number][category]
            source = result.GetValue() if result != 0 else ROOT.nullptr
            if result != 0:
                ROOT.optimized_histograms.fold_overflow(source)
            if category == plotCategory("kPlotEWKSSWW") or (
                category == plotCategory("kPlotQCDSSWW") and split_qcd
            ):
                targets = [plotCategory("kPlotEWKSSWW")] + [plotCategory(f"kPlotSignal{i}") for i in range(4)]
                for y_bin, target in enumerate(targets, 1):
                    histo_mva[number][target].SetBinError(1, 0.0)
                    ROOT.optimized_histograms.add_y_bin(histo_mva[number][target], source, y_bin)
            else:
                ROOT.optimized_histograms.add_y_bin(histo_mva[number][category], source, 1)


def materialize_ssww_auxiliaries(histo_ws, histo_nonprompt, histo_mva, active_categories, make_data_cards):
    """Retain SSWW charge and fake-rate templates, including empty samples."""
    if make_data_cards >= 1:
        # The legacy nj loop runs only nj=0: two regions, two charge shifts,
        # and six fake-rate shifts per region, even for samples with no entries.
        for index in range(4):
            if histo_ws[index] == 0:
                template = histo_mva[0 if index < 2 else 200][active_categories[0]]
                histo_ws[index] = empty_histogram(template, f"histoWS_{index}")
        for index in range(12):
            if histo_nonprompt[index] == 0:
                template = histo_mva[0 if index < 6 else 200][active_categories[0]]
                histo_nonprompt[index] = empty_histogram(template, f"histoNonPrompt_{index}")
