# -*- coding: UTF-8 -*-

from typing import Literal

import numpy as np
from anndata import AnnData
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

from .. import util as ul
from ..util import path, matrix_data, to_dense, sample_data

__name__: str = "plot_kde"


def kde(
    adata: AnnData,
    layer: str = None,
    title: str = None,
    width: float = 4,
    height: float = 2,
    axis: Literal[-1, 0, 1] = -1,
    sample_number: int = 1000000,
    output: path = None,
    show: bool = True
) -> None:
    if output is None and not show:
        ul.log(__name__).info(f"At least one of the `output` and `show` parameters is required")
    else:
        ul.log(__name__).info("Start plotting the Kernel density estimation chart")
        fig, ax = plt.subplots(figsize=(width, height))
        fig.subplots_adjust(bottom=0.3)
        data = adata.copy()

        # judge layers
        if layer is not None:

            if layer not in list(data.layers):
                ul.log(__name__).error("The `layer` parameter needs to include in `adata.layers`")
                raise ValueError("The `layer` parameter needs to include in `adata.layers`")

            data.X = data.layers[layer]

        if title is not None:
            plt.title(title)

        # Random sampling
        if axis == -1:
            matrix = sample_data(data.X, sample_number)
            sns.kdeplot(matrix, fill=True)
        elif axis == 0:
            if data.shape[0] * data.shape[1] > sample_number:
                col_number = data.shape[1]
                row_number: int = sample_number // col_number
                matrix: matrix_data = np.zeros((row_number, col_number))

                for i in range(col_number):
                    matrix[:, i] = sample_data(data.X[:, i], row_number)
            else:
                matrix = to_dense(data.X, is_array=True)

            sns.kdeplot(matrix, fill=True)
            ax.legend(list(adata.var.index))
        elif axis == 1:
            if data.shape[0] * data.shape[1] > sample_number:
                row_number = data.shape[0]
                col_number: int = sample_number // row_number
                matrix: matrix_data = np.zeros((row_number, col_number))

                for i in range(col_number):
                    matrix[i, :] = sample_data(data.X[i, :], col_number)
            else:
                matrix = to_dense(data.X, is_array=True)

            sns.kdeplot(matrix, fill=True)
            ax.legend(list(adata.obs.index))

        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.show()

        plt.close()
