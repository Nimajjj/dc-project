# Cinema API

## Routes
`[GET]` `/api/get/movie/<int:id_movie>/<string:option>`  
Request single movie by it's id.
`<string:option>` valid values:
    - `minimal`: return only movie datas and genres.  
    - `details`: return all datas including foreigns keys links.


---
Copyright (C) 2023 Borello Benjamin
