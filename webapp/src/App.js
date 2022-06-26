import { Container, createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import { BrowserRouter, Route, Router, Routes } from 'react-router-dom';
import './App.css';
import LandingForm from './Components/LandingForm';
import Map from './Components/Map';
import NavBar from './Components/NavBar';

const darkTheme = createTheme({
  palette: {
    mode: 'dark'
  }
})

function App() {
  return <>
  <CssBaseline />
    <ThemeProvider theme={darkTheme}>
      <NavBar />
      <Container style={{marginTop: '64px'}}>
        <BrowserRouter>
          <Routes>
            <Route path='/' element={<LandingForm />} />
            <Route path='/map' element={<Map />} />
          </Routes>
        </BrowserRouter>
      </Container>
    </ThemeProvider>
  </>
}

export default App;
