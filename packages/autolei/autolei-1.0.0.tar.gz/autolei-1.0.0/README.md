# AutoLEI

**Automated EffortLess MicroED Graphic User Interface (AutoLEI)** is an XDS-based GUI designed for real-time and batch processing of MicroED/3DED datasets. It provides a user-friendly platform for rapid, automated data processing and merging of multiple MicroED datasets, with well-designed and significantly streamlining structure determination workflows.

**Key Features**
- **User-Friendly Interface**: Simplifies MicroED data processing, requiring minimal manual input.
- **Batch Processing**: Handles large numbers of datasets with automated workflows.
- **Real-Time Data Processing**: Provides live feedback during data collection.
- **Versatility**: Supports diverse samples, including small molecules and proteins workflow.


---

## Installation

### Requirements
- **Operating Systems**: Linux or Windows via [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) (versions 1/2).
- **Software Dependencies**:
  - Python 3.8+ with libraries specified in `pyproject.toml`.
  - [XDS](https://xds.mr.mpg.de/) and [XDSGUI](https://wiki.uni-konstanz.de/xds/index.php/XDSGUI).
  - Optional tools: `xprep` for advanced features and LibreOffice for `.xlsx` files in Linux.

### Steps
1. Install via pip:
   ```bash
   pip install autolei
   ```
   For historical versions, use:
   ```bash
   pip install autolei-[version_name].zip
   ```
2. Manual installation:
   Follow the steps in the [Tutorial for AutoLEI](doc/AutoLEI_Tutorial.pdf) and [our Wiki](https://gitlab.com/395736627tristone/automicroedgui/-/wikis/home).

---

## Usage

### Command-line Usage
- **Launch the GUI**:
   ```bash
   autolei
   ```
   > *Note*: The first launch may take slightly longer as dependencies initialize.

- **Configure Settings**:
   ```bash
   autolei_setting
   ```
  The opened .ini file includes settings on screen scaling, multi-thread and report format.

- **Import Instrument**:
   ```bash
   autolei_add_instrument [instrument_setting_file]
   ```


### GUI pages
AutoLEI is organised into multiple working pages:
- **Input**: Configure experiment parameters and generate input files.
- **XDSRunner**: Automate initial processing and data quality inspection.
- **CellCorr**: Update unit cell information and refine settings.
- **XDSRefine**: Fine-tune processing parameters, including rotation axis and scaling.
- **MergeData**: Filter and merge datasets for downstream analysis.
- **Cluster&Output**: Perform clustering and generate outputs for structure determination.
- **Expert**: Miscellaneous tools for data reduction and PETS related function.
- **RealTime**: Live data processing with real-time feedback and automatic merging.

---

## Documentation
Detailed guides and examples can be found in:
- [Tutorial for AutoLEI](doc/AutoLEI_Tutorial.pdf)
- [Our Wiki](https://gitlab.com/395736627tristone/automicroedgui/-/wikis/home)

---

## Authors and Acknowledgments
Developed by Lei Wang and Yinlin Chen. Contributions from Gerhard Hofer, Hongyi Xu, and Xiaodong Zou at Stockholm University. The project integrates valuable resources from [edtools](https://github.com/instamatic-dev/edtools).

Supported by the European Union’s Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement no. 956099 (NanED − Electron Nanocrystallography−H2020-MSCAITN).

---
## License
The software is licensed under the BSD 3-Clause License.
