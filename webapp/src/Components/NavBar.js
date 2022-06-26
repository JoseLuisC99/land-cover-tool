import { AppBar, Toolbar, Typography } from "@mui/material";
import { Container } from "@mui/system";
import SatelliteAltIcon from '@mui/icons-material/SatelliteAlt';
import landing from './static/landing.css'


export default function NavBar() {
    return (
        <AppBar position="fixed" id="app-bar">
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                    <SatelliteAltIcon fontSize="large" style={{marginRight: '1rem', color: "#fff"}} />
                    <Typography variant="h6"
                        noWrap component="a" href="/"
                        sx={{
                            mr: 2, fontWeight: 700,
                            color: 'inherit', textDecoration: 'none',
                            flexGrow: 1, color: "#fff"
                        }}
                    >
                        Land Cover Tool
                    </Typography>
                    {/* <IconButton sx={{ ml: 1 }} color="inherit">
                        <Brightness7Icon /> 
                    </IconButton> */}
                </Toolbar>
            </Container>
        </AppBar>
    )
}