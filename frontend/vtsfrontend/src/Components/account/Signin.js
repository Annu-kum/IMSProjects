import React, { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import { InputLabel } from '@mui/material';
import { InputAdornment } from '@mui/material';
import {FormControl} from '@mui/material';
import { toast } from 'react-toastify';
// Define a default theme

const baseUrl='https://ims.digitaaz.com'
const defaultTheme = createTheme();

export default function LoginApp() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

 

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post(`${baseUrl}/accounts/userlogin/`,{
      username:username,
      password:password
    }).then(result =>{
      localStorage.setItem('Token',result.data.Token)
      toast.success("Login successfully")
      navigate('/over')

      //code to dateExpire...
      const tokenExpiration= 30*60*1000;
      const timeout =setTimeout(()=>{
        localStorage.removeItem('Token')
        navigate('/')
      },tokenExpiration)
      return () => clearTimeout(timeout);
    })
    .catch(err=>{
       toast.error("Invalid password")
       setUsername('')
       setPassword('')    
    })
  };

  return (
    <ThemeProvider theme={defaultTheme}>
    <Grid container component="main" sx={{ height: '100vh', background: `linear-gradient(${'#262828'},${'#5F85DB'},${'#262828'})` }}>
      <CssBaseline />
      <Grid
        item
        xs={12}
        sm={8}
        md={5}
        component={Box}
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
                     backgroundColor: '#fff',
          p: 4,
          borderRadius: 2,
          boxShadow: 3,
          margin: 'auto',
      
          
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: '#1B1A55' }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography style={{ fontWeight: 'bolder', fontSize: '18px' }}>
          IMS
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <FormControl variant="outlined" fullWidth>
            <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
            <OutlinedInput
              fullWidth
              id="password"
              type={showPassword ? 'text' : 'password'}
              value={password}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword}
                    edge="end"
                  >
                    {showPassword ? <Visibility /> : <VisibilityOff />}
                  </IconButton>
                </InputAdornment>
              }
              label="Password"
              name="password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </FormControl>
          <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label="Remember me"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2, bgcolor: '#1B1A55' }}
          >
            Sign In
          </Button>
          <Grid container>
            <Grid item xs>
             
            </Grid>
          </Grid>
        </Box>
      </Grid>
    </Grid>
  </ThemeProvider>
  );
}

