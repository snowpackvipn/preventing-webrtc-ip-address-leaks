# Data anonymisation scripts for publication

These Python scripts anonymise IP, MAC and FQDN data for the publication of this research work.

Fill the `constants.py` file with the data you want to anonymise and run `anonymise_all_txt.py` and `anonymise_all_pcapng.py`.

You can check the success of this operation with a `grep -i -r "data_to_anonymise" path_to_directory` command. This should not return anything in the standard output.