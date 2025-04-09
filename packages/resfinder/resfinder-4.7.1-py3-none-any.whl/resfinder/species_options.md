# Species options for ResFinder

The species option for ResFinder can take any scientific species name or
"other". A few species abbreviations are accepted, as written in the
"species_abbreviarions.md" file.
If the option "--ignore_missing_species" is set, then the application will not
complain if the given species is not recognized.
All recognized species have point mutation databases associated, but not all
recognized species have associated species panels associated. Species panels
indicate AMR relevant for a particular species.
The table below indicate which species are recognized by ResFinder.
If only genus is indicated, then all species within the genus are recognized.

## Species recognized by ResFinder

| Species                     | Point Mutation DB | Species Panels |
|-----------------------------|-------------------|----------------|
| Campylobacter               | yes               | yes            |
| Campylobacter coli          | yes               | yes            |
| Campylobacter jejuni        | yes               | yes            |
| Enterococcus faecalis       | yes               | yes            |
| Enterococcus faecium        | yes               | yes            |
| Escherichia coli            | yes               | yes            |
| Helicobacter pylori         | yes               | no             |
| Klebsiella                  | yes               | no             |
| Mycobacterium tuberculosis  | yes               | yes            |
| Neisseria gonorrhoeae       | yes               | no             |
| Plasmodium falciparum       | yes               | no             |
| Salmonella                  | yes               | yes            |
| Staphylococcus aureus       | yes               | yes            |
