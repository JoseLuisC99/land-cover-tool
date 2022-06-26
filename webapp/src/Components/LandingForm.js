import { Button, ButtonGroup, Card, CardContent, Container, Grid, Paper, TextField, Typography } from "@mui/material";
import { render } from "@testing-library/react";
import background from './static/background.mp4'
import landing from './static/landing.css'
import { useState } from "react";
import { Navigate } from "react-router-dom";

export default function LandingForm() {
    const [lat, setLatitude] = useState('')
    const [lon, setLongitude] = useState('')
    const [redirect, setRedirect] = useState(false)

    const onChangeLat = (e) => {
        setLatitude(e.target.value)
    }
    const onChangeLon = (e) => {
        setLongitude(e.target.value)
    }
    const sendRequest = (e) => {
        setRedirect(true)
    }

    return <>
        <video autoPlay muted id="bkgd-video">
            <source src={background} type="video/mp4" />
        </video>
        <div id="background-page"></div>
        <div id="form-container">
            <Card variant="outlined" align="center" id="input-card">
                <CardContent>
                    <Typography variant="h3" align="center">
                    Discover your environment
                    </Typography>
                    <Typography variant="h6" component="div" align="center" style={{marginBottom: '2rem'}}>
                    Con Land Cover Tool descubre y segmenta los diferentes tipos de terrenos y entornos que se encuentran al rededor de ti. Determina la cantidad de tierra agricola, forestal o cuerpos de agua en cualquier zona que quieras utilizando imagenes satelitales.  
                    </Typography>
                    <Typography sx={{fontSize: 14}} gutterBottom component="div">
                        Ingresa las coordenadas del sitio que deseas ver.
                    </Typography>
                    <ButtonGroup variant="container" style={{marginTop: '1rem'}}>
                        <TextField label="Latitud" variant="outlined" className="left-round" value={lat} onChange={onChangeLat} />
                        <TextField label="Longitud" variant="outlined" className="without-round" value={lon} onChange={onChangeLon} />
                        <Button 
                            variant="contained" className="right-round-button"
                            id="send-coords" onClick={sendRequest}
                        >
                            Enviar
                        </Button>
                    </ButtonGroup>
                </CardContent>
            </Card>
        </div>
        {redirect && <Navigate to={{
            pathname: '/map',
            search: `?lat=${lat}&lon=${lon}`
        }} replace={false} />}
    </>
}