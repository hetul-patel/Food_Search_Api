# Food Search API for Indian Dishes with spell correction and automatic word completion

Python Search API for Food Items with higher precision than SQL Like Query

Demo available at : http://flash-deploy.herokuapp.com/bunny/<Replace with dish name>

## Accurate query term match

search term: Pav Bhaji

* Results obtained from my API which can retrieve special cases like **Pav-Bhaji**, **PavBhaji** which MySQL LIKE query fail to fetch.
```

[
  {
    "0": 798,
    "1": "Pav Bhaji"
  },
  {
    "0": 1123,
    "1": "Pav Bhaji"
  },
  .
  .
  .
  .
  .
  {
    "0": 1189,
    "1": "Cheese PavBhaji"
  },
  {
    "0": 3224,
    "1": "Butter Pav-Bhaji"
  }
]

```

## Spell correction

* Search term: chynis nudles

```

[
  {
    "0": 3710,
    "1": "Stewed Noodles With Chinese Greens"
  }
]

```
