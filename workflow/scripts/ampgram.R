library(AmpGram)
library(AmpGramModel)
library(tidyverse)
library(parallel)

run_ampgram <- function(fasta) {
  prediction <- predict(AmpGram_model, fasta)
  return(prediction)
}

ampgram <- function(input, output) {
  input_fasta <- read_txt(input)
  splitted_fasta <- split(
    input_fasta,
    ceiling(seq_along(input_fasta) / 20)
  )
  ag <- mclapply(splitted_fasta, run_ampgram, mc.cores = snakemake@threads[[1]])
  ag1 <- map(ag, pred2df)
  nested_lists <- tibble(
    name = map(ag1, "seq_name"),
    ampgram = map(ag1, "probability")
  )

  ag2 <- unnest(nested_lists, cols = c(name, ampgram))

  ag2 %>%
    write_csv(output)
}

ampgram(snakemake@input[[1]], snakemake@output[[1]])
