# metagrapho-tropy

Add transcriptions to items in Tropy using the Transkribus metagrapho API.

## AB proof of concept

1. input tropy_export JSON-LD
2. if an item has type `Foto`, select the second image of the object (= backside) for processing
3. optional: check if text is handwritten, check text orientation
4. get the image via the filepath
5. transform the image to base64
6. process the image (and optional parameters wrt models for layout analysis, atr) via `TranskribusProcessingAPI.post_process`
7. get the transcription via `TranskribusProcessingAPI.get_result`
8. add note with transcription to item in tropy_export JSON-LD
9. optional: map Transcribus text region coordinates (or line coordinates) to Tropy selection, add selection to item in tropy_export JSON-LD
