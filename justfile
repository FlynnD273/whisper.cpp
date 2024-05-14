@init:
  #!/usr/bin/bash
  bash ./models/download-ggml-model.sh tiny.en
  bash ./models/download-ggml-model.sh tiny
  bash ./models/download-ggml-model.sh base.en
  bash ./models/download-ggml-model.sh base
  bash ./models/download-ggml-model.sh medium.en
  bash ./models/download-ggml-model.sh medium
  make quantize
  ./quantize models/ggml-medium.bin models/ggml-medium-q.bin q5_0
