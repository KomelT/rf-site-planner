# RF Site Planner
<a href="https://hub.docker.com/r/komelt/rf-site-planner-app" target="_blank">![APP](https://img.shields.io/badge/APP-blue?logo=Docker)</a>
<a href="https://hub.docker.com/r/komelt/rf-site-planner-api" target="_blank">![API](https://img.shields.io/badge/API-blue?logo=Docker)</a>
<a href="https://hub.docker.com/r/komelt/splat-python" target="_blank">![Splat Python](https://img.shields.io/badge/Splat_Python-blue?logo=Docker)</a>

![App screenshot](./assets/screenshot.png)

## Development

### Updating API requirements
```bash
cd api
pipreqs --force .
```

## Splat
- [Website](https://www.qsl.net/kd2bd/splat.html)
- [Documentaion](https://www.qsl.net/kd2bd/splat.pdf)

### Elevation data source
Elevation data was downloaded from [viewfinderpanoramas.org](https://viewfinderpanoramas.org/).
- [1" download map](https://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org1.htm)
- [3" download map](https://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm)

**Command to convert .hgt into Splat Data File .sdf**\
Use `srtm2sdf` for 3" datafiles and `srtm2sdf-hd` for 1" datafiles.
```bash
for file in ../*.hgt; do srtm2sdf -d . $file; done
```

## Helpful Splat info
- [jeremyclark.ca/wp/telecom/splat-antenna-patterns](https://jeremyclark.ca/wp/telecom/splat-antenna-patterns/)

## Credits
This project is based on code from [Meshtatsic Site Planner](https://github.com/meshtastic/meshtastic-site-planner)