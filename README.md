# EXAMM vis
Parses fitness logs that examm spits out. If you change the outputs of the fitness log, you may have to modify the DataPoint class in `analysis/fitness_log.py`.

# Assumed File Layout
The `FitnessLogBatch` class reads n runs from a given results folder. The results folder must be of the format:

```
└── results
    ├── 0
    │   └── fitness_log.md
    ├── 1
    │   └── fitness_log.md
    ├── ...
    │
    └── n - 1
        └── fitness_log.md
```
