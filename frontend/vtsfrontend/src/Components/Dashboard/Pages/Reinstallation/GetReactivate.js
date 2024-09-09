import React, { useState,useEffect } from 'react';
import axios from 'axios';
import { useForm, Controller } from 'react-hook-form';
import { TextField, Table, TableBody, TableCell, TableContainer,Alert, TableHead, TableRow, Paper, Checkbox, Button } from '@mui/material';


import TablePagination from '@mui/material/TablePagination';

import { IconButton, MenuItem, Typography, Hidden } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { v4 as uuid } from 'uuid';

import Grid from '@mui/material/Unstable_Grid2/Grid2';
import { Box } from '@mui/material';
// import Dateview from './DateView';
import { DataGrid, gridColumnVisibilityModelSelector, } from '@mui/x-data-grid';
import Dateview from '../Manages/Installation/DateView';
import  '../Manages/Installation/install.css';
import Header from '../../Header';
import { useTheme } from '@mui/material';
import useMediaQuery from '@mui/material/useMediaQuery';

import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
const columns = [
  { id: '', label: 'Action'},
  {id:'vehicle1',label: 'Vehicle No 1',minWidth: 120,align: 'right', format: (value) => value.toFixed(2), },
  { id: 'Entity_id', label: 'Entity ID', minWidth: 150 },
  {id: 'ReactivationDate',label: 'Reactivation Date',minWidth: 150,align: 'right',format: (value) => value.toFixed(2),},
    
  { id: 'MILLER_NAME', label: ' MILLER NAME', minWidth: 150 },
  { id: 'MillerContactNo', label: 'Miller ContactNo', minWidth: 180 },
  { id: 'district', label: 'District', minWidth: 120 },
  { id: 'GPS_IMEI_NO', label: 'GPS IMEI No', minWidth: 150 },
  { id: 'SIM_NO', label: 'SIM No', minWidth: 100, align: 'right' },
  { id: 'Device_Name', label: 'Device Name', minWidth: 120, align: 'right' },
  { id: 'Dealer_Name', label: 'Dealer Name', minWidth: 120, align: 'right' },
  // Add more columns as needed
  {id: 'NewRenewal',label: 'New/Renawal',minWidth: 120,align: 'right',format: (value) => value.toFixed(2),},
  {id: 'OTR',label: 'OTR',minWidth: 80,align: 'right', format: (value) => value.toFixed(2),},
  { id: 'vehicle2', label: 'Vehicle No 2', minWidth: 120, align: 'right', format: (value) => value.toFixed(2),},
  {id: 'vehicle3', label: 'Vehicle No 3', minWidth: 120, align: 'right', format: (value) => value.toFixed(2),},
 
      {
        id: 'Employee_Name',
        label: ' Employee Name ',
        minWidth: 120,
        align: 'right',
        format: (value) => value.toFixed(2),
      },
      {
        id: 'Device_Fault',
        label: 'Device Fault ',
        minWidth: 150,
        align: 'right',
        format: (value) => value.toFixed(2),
      },
      {
        id: 'Fault_Reason',
        label: 'Fault Reason',
        minWidth: 150,
        align: 'right',
        format: (value) => value.toFixed(2),
      },
      {
        id: 'Replace_DeviceIMEI_NO',
        label: 'Replace Device IMEI No',
        minWidth: 170,
        align: 'right',
        format: (value) => value.toFixed(2),
      },
      {
        id: 'Remark1',
        label: 'Remark 1',
        minWidth: 100,
        align: 'right',
        format: (value) => value.toFixed(2),
      },
     {
        id: 'Remark2',
        label: 'Remark 2',
        minWidth: 100,
        align: 'right',
        format: (value) => value.toFixed(2),
     },
      {
        id: 'Remark3',
        label: 'Remark 3',
        minWidth: 100,
        align: 'right',
        format: (value) => value.toFixed(2),
      },     
];



const InputTable = () => {
  
  const [millerId, setMillerId] = useState('');
  const [dealername,setDealername] = useState('');
  const [installations, setInstallations] = useState([]);
  const [selectedRows, setSelectedRows] = useState([]);
  const { control, handleSubmit } = useForm();
  const [file, setFile] = useState(null);
  const token = localStorage.getItem('Token');
  const headers = {
    'content-type': 'application/json',
    'Authorization': `Token ${token}`,
    'Accept': 'application/json',
  };
  const isNonMobile = useMediaQuery("(min-width:600px)");
  const[loadDealers,setLoadealers]=useState([])



  const fetchInstallations = async () => {
    try {
      const response = await axios.get(`https://ims.digitaaz.com/deactivation/getdeactivate/${millerId}/`, { headers });
      setInstallations(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error fetching installations:', error);
    }
  };

  

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleRowSelect = (id) => {
    setSelectedRows((prevSelectedRows) =>
      prevSelectedRows.includes(id)
        ? prevSelectedRows.filter((rowId) => rowId !== id)
        : [...prevSelectedRows, id]
    );
  };
  const [open, setOpen] = useState(true);

 


  const onSubmit = async (data) => {
    const selectedData = installations
      .filter((installation) => selectedRows.includes(installation.id))
      .map((installation) => ({
        ...installation,
        ...data[installation.id],
        MILLER_TRANSPORTER_ID:millerId,
        Reactivation_letterHead:file, // Add the deactivation letterhead to each selected row
      }));

   
        selectedData.forEach((row) => {
          const formData = new FormData();
          Object.keys(row).forEach(key => formData.append(key, row[key]));
           
            formData.append('MILLER_TRANSPORTER_ID', millerId);
            formData.append('Reactivation_letterHead', file);
          axios.post(`https://ims.digitaaz.com/reactivation/postReactivate/`,formData,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${token}`
          },}
          )
            .then((res) => 
              toast.success("Data submitted successfully ",{
                theme:"light",
                position:"top-center"
              })).catch((err) => 
              alert("check date or letterhead field")
              
      );
        });
          };

  return (
    <Paper sx={{ width:'100%', overflow: 'hidden', }}>
  
    <Box m="20px">
         {/* HEADER */}
         <Box display="flex" justifyContent="space-between" alignItems="center">
         <Header title="Device Entry" subtitle={'Entry of Reactivated Device'} />
          
         </Box>
   
         {/* First Box*/}
         <Box
              backgroundColor='#F0F8FF'
             padding={'1.5rem'}
             m={'0px 0px 12px'}
             borderRadius={'1%'}
             boxShadow={'12'}
           >
             
             <Box
                 display="grid"
                 gap="15px"
                 gridTemplateColumns="repeat(3, minmax(0, 1fr))"
                 sx={{
                   "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
                 }}
               >
                 <Box sx={{ fontWeight: 'bold' }}>
                   <label>Miller/Transporter Id</label>      
               <TextField
               fullWidth
              
               type="text"
    
        value={millerId}
        onChange={(e)=>setMillerId(e.target.value)}
        sx={{ gridColumn:'span 2' ,color:'black'}}
        InputProps={{sx:{height:'40px'}}}
        
      />
          
                 <Button
                   sx={{
                     height:'6vh',
                     width:'40px',
                     background:`linear-gradient(${'#233044'},${'#233044'})`,
                     '&:hover':{
                       background:'#9290C3',
                       color:'#fff',
                       fontSize: "14px",
                     fontWeight: "bold",
                     
                     },
                     color:'#fff' ,
                     fontSize: "14px",
                     fontWeight: "bold",
                     gridColumn:'span 2',
                     margin:'15px 0px 0px 0px'
                    }}
                    onClick={fetchInstallations}
                 >Load
                 </Button>
                 </Box>  
                
                 <Box sx={{ fontWeight: 'bold' }}>
                 <Typography  sx={{fontFamily:'inherit',fontWeight:'bold',color:'black',fontSize:'15px' }}>Upload LetterHead <IconButton sx={{color:'red'}}>*</IconButton></Typography>
                 <input
                             type="file"
                             accept=".pdf,.doc,.docx,.png"
                             onChange={handleFileChange}
                             
                             required
                          />
                          </Box>
                 </Box>
                 </Box>  
           {/* Row 2 */}
            <Box
             gridColumn="span 4"
             gridRow="span 2"
             backgroundColor='#F0F8FF'
             p="8px"
             boxShadow={'12'}
           >
             
             <Box m="1.5rem ">
         <Box
           height="100%"
           sx={{
             "& .MuiDataGrid-root": {
               border: "none",
             },
             "& .MuiDataGrid-cell": {
               borderBottom: "none",
             },
             "& .MuiDataGrid-columnHeaders": {
               bgcolor:'none',
               color: 'none',
               borderBottom: "none",
               
             },
             "& .MuiDataGrid-virtualScroller": {
               backgroundColor: 'none',
             },
             "& .MuiDataGrid-footerContainer": {
               backgroundColor: 'none',
               color: 'none',
               borderTop: "none",
             },
             "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
               color: `none !important`,
             },
            
           }}
         >
          <form onSubmit={handleSubmit(onSubmit)}>
      <TableContainer sx={{ maxHeight: 300, borderRadius:'1%'}}>
        <Table stickyHeader aria-label="sticky table" size='small'>
          <TableHead>
          <TableRow   >
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={'center'}
                  style={{ minWidth: column.minWidth,minHeight:10,background: '#233044' ,color:'#fff',fontFamily:'sans-serif',fontWeight:'bold',border:'1px solid white' }}   
               >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {installations.length > 0 ? (
              installations.map((installation) => (
                <TableRow key={installation.id}>
                  <TableCell>
                    <Checkbox
                      checked={selectedRows.includes(installation.id)}
                      onChange={() => handleRowSelect(installation.id)}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.vehicle1`}
                      control={control}
                      defaultValue={installation.vehicle1}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small"  />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Entity_id`}
                      control={control}
                      defaultValue={installation.Entity_id}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.ReactivationDate`}
                      control={control}
                      defaultValue={installation.DeactivationDate}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" type="date" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.MILLER_NAME`}
                      control={control}
                      defaultValue={installation.MILLER_NAME}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.MillerContactNo`}
                      control={control}
                      defaultValue={installation.MillerContactNo}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.district`}
                      control={control}
                      defaultValue={installation.district}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.GPS_IMEI_NO`}
                      control={control}
                      defaultValue={installation.GPS_IMEI_NO}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.SIM_NO`}
                      control={control}
                      defaultValue={installation.SIM_NO}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Device_Name`}
                      control={control}
                      defaultValue={installation.Device_Name}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Dealer_Name`}
                      control={control}
                      defaultValue={installation.Dealer_Name}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.NewRenewal`}
                      control={control}
                      defaultValue={installation.NewRenewal}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small"  />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.OTR`}
                      control={control}
                      defaultValue={installation.OTR}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                 
                  <TableCell>
                    <Controller
                      name={`${installation.id}.vehicle2`}
                      control={control}
                      defaultValue={installation.vehicle2}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small"  />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.vehicle3`}
                      control={control}
                      defaultValue={installation.vehicle3}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small"  />}
                    />
                  </TableCell>
                  
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Employee_Name`}
                      control={control}
                      defaultValue={installation.Employee_Name}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Device_Fault`}
                      control={control}
                      defaultValue={installation.Device_Fault}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small"  />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Fault_Reason`}
                      control={control}
                      defaultValue={installation.Fault_Reason}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small"  />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Replace_DeviceIMEI_NO`}
                      control={control}
                      defaultValue={installation.Replace_DeviceIMEI_NO}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small"  />}
                    />
                  </TableCell>
 
                  
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Remark1`}
                      control={control}
                      defaultValue={installation.Remark1}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Remark2`}
                      control={control}
                      defaultValue={installation.Remark2}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  <TableCell>
                    <Controller
                      name={`${installation.id}.Remark3`}
                      control={control}
                      defaultValue={installation.Remark3}
                      render={({ field }) => <TextField {...field} variant="outlined" size="small" />}
                    />
                  </TableCell>
                  
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan="10">No Data found</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <Button type="submit" 
      sx={{
        background:`linear-gradient(${'#233044'},${'#82A0D8'})`,
        '&:hover': {
          backgroundColor: '#1B1A55',
          color: '#fff',
          fontSize: "12px",
          fontWeight: "bold",
        },
        color: '#fff',
        fontSize: "12px",
        fontWeight: "bold",
        height: '30px',
        margin: '25px 0px 0px 0px'
      }}
      >
        Submit Selected Rows
      </Button>
      <Button
                sx={{
                  background:`linear-gradient(${'#FF8E8F'},${'#D04848'})`,
                  '&:hover': {
                    backgroundColor:'#FF8A08',
                     color: '#fff',
                    fontSize: "12px",
                    fontWeight: "bold",
                  },
                  color: '#fff',
                  fontSize: "12px",
                  fontWeight: "bold",
                  height: '30px',
                  margin: '25px 0px 0px 5px'
                }}
              >Cancel
              </Button>
    </form>
   
   
         </Box>
       </Box> 
        </Box>  
       
             
             </Box>
       </Paper>
  );
};

export default InputTable;




