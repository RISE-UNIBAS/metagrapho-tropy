# metagrapho-tropy

Add transcriptions to items in Tropy using the Transkribus metagrapho API.

## Creator

This dataset was created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in 2023.

## File structure and data overview

Note that there are [different versions of this dataset](https://github.com/RISE-UNIBAS/metagrapho-tropy/releases).

- Python package in [/metagrapho_tropy](https://github.com/RISE-UNIBAS/metagrapho-tropy/tree/main/metagrapho_tropy)
- sample data in [/sample](https://github.com/RISE-UNIBAS/metagrapho-tropy/tree/main/sample)

## Tutorial

```
from metagrapho_tropy.client import Client

Client().process_tropy(tropy_file_path="sample_input.json",
                       item_type="Foto",
                       item_image_index=1)
Client().download(mapping_file_path="mapping_input.csv")
Client().enrich_tropy(tropy_file_path="sample_input_updated.json",
                      download_file_path="download_input.json",
                      lines=True)
```

## To dos

- [ ] add unittests based on sample data
- [ ] add documentation via Sphinx and pages
- [ ] flesh out tutorial
- [x] add CITATION.cff
- [ ] release with Zenodo DOI
- [ ] add metadata on transcription provenance

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
