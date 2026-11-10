# Changelog

Notable changes to the Python Speech Center client. Add an entry under
**Unreleased** in the same PR as the change.

## [Unreleased]

### Changed
- TTS examples in the Makefile (`help-tts`) now use `helena_es_es` instead of the
  Verbio voice `david_es_es`. Speech Center is removing the Verbio TTS voices
  (`david_es_es`, `miguel_es_pe`, `luz_es_pe`, `eduardo_pt_br`, `anna_ca_es`), and
  Peruvian Spanish (`es-PE`) along with them (SC2-4120). See the
  [available voices](https://doc.speechcenter.verbio.com/#tag/Text-To-Speech-Common-Features/Available-voices)
  for the current list and the documentation changelog for suggested replacements.
