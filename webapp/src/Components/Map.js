import { useEffect, useRef, useState } from "react"
import env from "../env"
import axios from "axios"
import { Alert, BottomNavigation, BottomNavigationAction, Paper, Skeleton, Snackbar } from "@mui/material"
import "./static/map.css"
import FavoriteIcon from '@mui/icons-material/Favorite';

export default function Map() {
    const [lat, setLatitude] = useState('')
    const [lon, setLongitude] = useState('')
    const [loading, setLoading] = useState(true)
    const [filter, setFilter] = useState(0)
    const [urlImage, setURLImage] = useState([])
    const initialRender = useRef(true)

    const loadGoogleMaps = () => {
        const script = document.createElement('script')
        script.src = "/map.js"
        document.body.appendChild(script)

        const maps = document.createElement('script');
        maps.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyC8wKQkCvnGCAoPV1b15IPk2zuDP1tcMBE'
        document.body.appendChild(maps)
        return () => {
            document.body.removeChild(maps);
            document.body.removeChild(script);
        }
    }

    useEffect(() => {
        if(initialRender.current) {
            initialRender.current = false
            loadGoogleMaps()
            const search = window.location.search
            const params = new URLSearchParams(search)
            const lat = params.get('lat')
            const lon = params.get('lon')
            setLatitude(lat)
            setLongitude(lon)

            const url_map = `https://maps.googleapis.com/maps/api/staticmap?center=${lat},${lon}&zoom=17&size=1280x960&maptype=satellite&key=${env.API_KEY}`
            axios.get(url_map, {responseType: 'arraybuffer'}).then(res => {
                const img = res.data
                const blob = new Blob([img], { type: 'image/png' });
                const formData = new FormData()
                formData.append('images', blob)
                axios.post('http://localhost:8080/api/v1/predict', formData).then(res => {
                    const images = res.data
                    setLoading(false)
                    const land_names = ['Urban land', 'Agriculture land', 'Rangeland', 'Forest land', 'Water', 'Barren land']
                    for(let i=0; i<land_names.length; i++) {
                        const img = images[land_names[i]]
                        urlImage.push(`data:image/png;base64,${img}`)
                    }
                })
            })
            setTimeout(() => {
                window['iniciarMap'](parseFloat(lat), parseFloat(lon))
            }, 500)
        }
    }, [])
    return <>
        <div id="map"></div>
        <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={3}>
            <BottomNavigation showLabels
                value={filter} onChange={(e, newValue) => {setFilter(newValue)}}
            >
                <BottomNavigationAction label="Tierra urbana" />
                <BottomNavigationAction label="Tierra agrícola" />
                <BottomNavigationAction label="Pastizales" />
                <BottomNavigationAction label="Tierra forestal" />
                <BottomNavigationAction label="Agua" />
                <BottomNavigationAction label="Tierra estéril" />
            </BottomNavigation>
        </Paper>
        {!loading ? (
            <img src={urlImage[filter]} id="image-filter" />
        ) : (
            <Skeleton variant="rectangular" id="skeleton-filter" />
        )}
        {loading && <Snackbar 
            anchorOrigin={{vertical: 'top', horizontal: 'right'}}
            open={loading}
        >
            <Alert variant="filled" severity="warning" className="fillAlert">
                Cargando y segmentando terreno.
            </Alert>
        </Snackbar> }
    </>
}