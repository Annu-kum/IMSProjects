import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Dateview from '../Manages/Installation/DateView';
import {CSVLink,CSVDownload} from 'react-csv';
import  {useTheme } from '@mui/material';
import {
  GridToolbarContainer,
  GridToolbarFilterButton,
} from '@mui/x-data-grid';
import jspdf from 'jspdf';
import 'jspdf-autotable';
import Search from '../Manages/Installation/Search';
import '../Manages/Installation/install.css'
import {Typography,TableCell,TableRow,TableContainer,Table,TableHead,TableSortLabel,TableBody,TablePagination} from '@mui/material';
import axios from 'axios';
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import RefreshIcon from '@mui/icons-material/Refresh';
import {CircularProgress} from '@mui/material';



export default function   ReactivationReport() {
  const [rows, setRows] = React.useState([]);
  const [rowModesModel, setRowModesModel] = React.useState({});
  const [DataFromChild,setDataFromChild]=React.useState('')
  const theme = useTheme()
  const [page,pageChange]=React.useState(0);
  const [loading, setLoading] = React.useState(true);
  const[rowsPerPage,rowperpagechange]=React.useState(25);
  const [order, setOrder] = React.useState()
  const [orderBy, setOrderBy] = React.useState()
  const [startDate,setStartRange]=React.useState(new Date())
  const [endDate,setEndRanges]=React.useState(new Date())
  const [search,setSearch]=React.useState('')
  const token = localStorage.getItem('Token');
 const headers = {
   'content-type': 'application/json',
   'Authorization': `Token ${token}`,
   'Accept': 'application/json',
 };




  //columns of the table...
  const columns = [
    { field: 'Entity_id',align:'center', label: 'Entity Id', width: 100,  },
    { field: 'district',align:'center',  label: 'District', width: 100, sx:{fontFamily:'cursive'} },
    { field: 'GPS_IMEI_NO',align:'center', label: 'GPS IMEI NO', width: 100,  },
    { field: 'SIM_NO',align:'center',  label: 'SIM NO', width: 100, },
    { field: 'Device_Name',align:'center', label: 'Device Name', width: 100, },
    { field: 'Dealer_Name',align:'center', label: 'Dealer Name', width: 100,  },
    { field: 'NewRenewal',align:'center', label: 'New/Renewal', width: 100, },
    { field: 'OTR',align:'center',label: 'OTR', width: 100, },
    { field: 'vehicle1',align:'center',  label: 'Vehicle No 1', width: 100, },
    { field: 'vehicle2',align:'center',  label: 'Vehicle No 2', width: 100,  },
    { field: 'vehicle3',align:'center',  label: 'Vehicle No 3', width: 100,  },
    { field: 'MILLER_TRANSPORTER_ID', align:'center',label: 'Miller/Transporter Id', width: 100,},
    { field: 'MILLER_NAME',align:'center',  label: 'Miller/Transporter Name', width: 100, },
    { field: 'MillerContactNo',align:'center', label: 'MillerContactNo', width: 100, },
    { field: 'ReactivationDate',align:'center',  label: 'Reactivation Date', width: 100 },
    // { field: 'Installation_letterHead',align:'center', headerAlign:'center', label: 'Installation Letterhead', width: 180, editable: false ,headerClassName:'head',},
    // {
    //   field: 'download',
    //   label: 'Download',
    //   headerAlign:'center',
    //   width: 10,
    //   editable: false,
    //   align:'center',
    //   headerClassName: 'head',
    //   renderCell: (params) => (
    //     <IconButton
    //       variant="contained"
    //       onClick={handleDownload(params.row.id)}
    //     >
    //     <DownloadIcon/>
    //     </IconButton>
    //   ),
    // },
    { field: 'Employee_Name',align:'center',  label: 'Entry Employee Name', width: 100,  },
    { field: 'Device_Fault',align:'center',  label: 'Device Fault' ,width:100,  },
    { field: 'Fault_Reason',align:'center', label: 'Fault Reason', width: 100,  },
    { field: 'Replace_DeviceIMEI_NO',align:'center', label: 'Replace Device IMEI No', width: 100,  },
    { field: 'Remark1', align:'center',label: 'Remark 1', width: 100, },
    { field: 'Remark2',align:'center', label: 'Remark 2', width: 100, },
    { field: 'Remark3',align:'center', label: 'Remark 3', width: 100,},
  ];


  const getData = async (start, end) => {
    setLoading(true)
    try {
      // Function to format the date to 'DD-MM-YYYY'
      const formatDate = (date) => {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // getMonth() returns month from 0-11
        const year = date.getFullYear();
        return `${day}-${month}-${year}`;
      };
  
      const formattedStartDate = start ? formatDate(start) : undefined;
      const formattedEndDate = end ? formatDate(end) : undefined;
  
      const response = await axios.get(`https://imsapi.digitaaz.com/reactivation/getReactivatedetai/`, {
        params: {
          start_date: formattedStartDate,
          end_date: formattedEndDate,
        },
        headers
      });
  
      setRows(response.data);
    } catch (error) {
      toast.error("Something went wrong");
    }finally{
      setLoading(false)
    }
  };


    React.useEffect(() => {
      getData(startDate, endDate);
    }, [startDate, endDate]);
  


  const refreshBtn=()=>{
    getData()
  }

  const handlechangepage=(event,newPage)=>{
    pageChange(newPage)
  }
  const handleRowsPerPage =(e)=>{
    rowperpagechange(+e.target.value)
    pageChange(0)
  }

  const handleDownload = (id) => async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `https://imsapi.digitaaz.com/deactivation/get_file_url/${id}/`,
        responseType: 'arraybuffer',
      });

      const contentType = response.headers['content-type'];
      const blob = new Blob([response.data], { type: contentType });
      const fileUrl = window.URL.createObjectURL(blob);

      // Get filename from content-disposition header
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'Deactivation_letterhead';
      if (contentDisposition) {
        const matches = /filename="(.+)"/.exec(contentDisposition);
        if (matches != null && matches[1]) {
          filename = matches[1];
        }
      }

      // Initiate download
      const link = document.createElement('a');
      link.href = fileUrl;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading file:', error);
      toast.error('Error downloading file');
    }
  };
 
  
  

  const pdfs = () => {
    const doc = new jspdf({orientation:'landscape'});
    doc.text('Reactivation Report', 12, 10);
    doc.autoTable({
      columns: columns.map(col => ({ 
        header: col.label, 
        dataKey: col.field, 
        columnWidth: 10 // or a specific width, e.g. 50
        
      })),

      tableLineWidth: 0,
     
      pageSize:'A0',
      cellWidth: 8,
      body: filteredRows,

      headStyles: {
        fontSize: 8.5, // adjust font size to fit the width
        halign: 'center', // center the header text
        margin: { top: 1, },  
        
        lineColor: [0, 0, 0] // black border
      },
      theme: 'grid', // or 'triped' or 'plain'
      startY: 15,
      // split overflowing columns into pages
      horizontalPageBreak: true,
      horizontalPageBreakBehaviour: 'immediately',
    });
    doc.save('Reactivation Report.pdf');
  };

  //PDF Converter....
//   function pdfs(){
//     const doc=new jspdf()
//     doc.text('Installation Table',12,12)
//     doc.autoTable({
//       theme:'grid',
//       columns:[
//         {header:'District',dataKey:'district'},
//         {header:'GPS IMEI No',dataKey:'gpsImeiNo'},
//         {header:'SIMNo',dataKey:'simNo'},
//         {header:'Device Name',dataKey:'deviceName'},
//         {header:'DEALER NAME',dataKey:'DEALERNAME'},
//         {header:'New Renewal',dataKey:'NEW_RENEWAL'},
//         {header:'OTR',dataKey:'OTR'},
//         {header:'VehicleNo1',dataKey:'VehicleNo1'},
//         {header:'VehicleNo2',dataKey:'VehicleNo2'},
//         {header:'VehicleNo3',dataKey:'VehicleNo3'},
//         {header:'MILLER_TRANSPORTER_ID',dataKey:'MILLER_TRANSPORTER_ID'},
//         {header:'MILLER_TRANSPORTER_NAME',dataKey:'MILLER_TRANSPORTER_NAME'},
//         {header:'Miller_contactNo',dataKey:'Miller_contactNo'},
//         {header:'InstallationDate',dataKey:'InstallationDate'},
//         {header:'Installed_LETTERHEAD',dataKey:'Installed_LETTERHEAD'},
//         {header:'EMPLOYEE_NAME',dataKey:'ENTRY_EMPLOYEE_NAME'},
//         {header:'DEVICE_FAULTY',dataKey:'DEVICE_FAULTY'},
//         {header:'FAULTY_REAON',dataKey:'FAULTY_REAON'},
//         {header:'REPLACE_DEVICE_IMEI_NO',dataKey:'REPLACE_DEVICE_IMEI_NO'},
//         {header:'REMARK_1',dataKey:'REMARK_1'},
//         {header:'REMARK_2',dataKey:'REMARK_2'},
//         {header:'REMARK_3',dataKey:'REMARK_3'},

// ],
//         body:rows,
//     })
//     doc.save()
//   }
  //Groups of buttons...
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
 
  

  //Get data From search bar....
  const rowStyles = {
    redRow: {
      backgroundColor: 'red',
      color: 'white',
    },
  };

  
  // filter according to date 

  const DateFilter = (start,end) => {
    React.useEffect(() => {
      if (start && end) {
        setStartRange(start);
        setEndRanges(end);
      }
    },[]
  )}
  // const dateFilter =(start,end)=>{
  //      setStartRange(start)
  //      setEndRanges(end)
       
  // }
  // console.log(startDate,endDate)
  //Code for filtering data....
  const filterRowsBySearch = () => {
  
    return rows.filter(row => {
     
      const matchesSearch = Object.values(row).some(value => String(value).toLowerCase().includes(search.toLowerCase()));
    
      return matchesSearch ;
    });
  };
  //filterData of the rows...
  const filteredRows = filterRowsBySearch();

  const getRowClassName = (params) => {
    return params.indexRelativeToCurrentPage % 2 === 0 ? 'even' : 'odd';
    
  };

function CustomToolbar() {
    return (
      <div style={{ order: 1 }}>
        <GridToolbarContainer>
          <GridToolbarFilterButton />
        </GridToolbarContainer>
      </div>
    );
  }

  const [value, setValue] = React.useState(1);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  const handleSortRequest = cellId => {
    const isAsc = orderBy === cellId && order === "asc";
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(cellId)
}
function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) return order;
      return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

function getComparator(order, orderBy) {
  return order === 'desc'
      ? (a, b) => descendingComparator(a, b, orderBy)
      : (a, b) => -descendingComparator(a, b, orderBy);
}

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
      return -1;
  }
  if (b[orderBy] > a[orderBy]) {
      return 1;
  }
  return 0;
}

const csvHeaders = [
  { key: 'Entity_id',align:'center', label: 'Entity Id', width: 100,  },
{ key: 'district',align:'center',  label: 'District', width: 100, sx:{fontFamily:'cursive'} },
{ key: 'GPS_IMEI_NO',align:'center', label: 'GPS IMEI NO', width: 100,  },
{ key: 'SIM_NO',align:'center',  label: 'SIM NO', width: 100, },
{ key: 'Device_Name',align:'center', label: 'Device Name', width: 100, },
{ key: 'Dealer_Name',align:'center', label: 'Dealer Name', width: 100,  },
{ key: 'NewRenewal',align:'center', label: 'New/Renewal', width: 100, },
{ key: 'OTR',align:'center',label: 'OTR', width: 100, },
{ key: 'vehicle1',align:'center',  label: 'Vehicle No 1', width: 100, },
{ key: 'vehicle2',align:'center',  label: 'Vehicle No 2', width: 100,  },
{ key: 'vehicle3',align:'center',  label: 'Vehicle No 3', width: 100,  },
{ key: 'MILLER_TRANSPORTER_ID', align:'center',label: 'Miller/Transporter Id', width: 100,},
{ key: 'MILLER_NAME',align:'center',  label: 'Miller/Transporter Name', width: 100, },
{ key: 'MillerContactNo',align:'center', label: 'MillerContactNo', width: 100, },
{ key: 'DeactivationDate',align:'center',  label: 'Deactivation Date', width: 100 },

{ key: 'Employee_Name',align:'center',  label: 'Entry Employee Name', width: 100,  },
{ key: 'Device_Fault',align:'center',  label: 'Device Fault' ,width:100,  },
{ key: 'Fault_Reason',align:'center', label: 'Fault Reason', width: 100,  },
{ key: 'Replace_DeviceIMEI_NO',align:'center', label: 'Replace Device IMEI No', width: 100,  },
{ key: 'Remark1', align:'center',label: 'Remark 1', width: 100, },
{ key: 'Remark2',align:'center', label: 'Remark 2', width: 100, },
{ key: 'Remark3',align:'center', label: 'Remark 3', width: 100,},
];

  return (
    <>
       {/* First Box*/}
       <Box
            backgroundColor='#F0F8FF'
           padding={'0rem'}
           m={'0px 0px 1px'}
           borderRadius={'1%'} 
           alignItems='flex-end'  
           position={'relative'}
           zIndex={'12'} 
         > 
           <Box
               display="grid"
               gridTemplateColumns="repeat(2, minmax(0, 1fr))"
               sx={{
                //  "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
               }}
             >
     
             <Box p='10px'>
             <Search sendData={setSearch}/>
             </Box>
             <Box p='2px' sx={{display:'flex',justifyContent:'flex-end'}}  >
             
               <Dateview getData={DateFilter}/>
             
             {/* Export Button */}
    <Button
        id="demo-positioned-button"
        aria-controls={open ? 'demo-positioned-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
        sx={{backgroundColor: '#1B1A55',
        '&:hover':{
          backgroundColor:'#1B1A55',
          color:'#fff',
          fontSize: "12px",
        fontWeight: "bold",
       
        },
        color:'#fff' ,
        fontSize: "12px",
        fontWeight: "bold",
        height:'30px',
        margin:'25px 0px 0px 0px'
       
       }}
      >
        <CSVLink filename="Reactivation_report.csv" headers={csvHeaders} data={filteredRows} style={{textDecoration:'none',color:'inherit'}}>Export</CSVLink>
      </Button>
     
      <Box ><Button 
    sx={{
      backgroundColor: '#fff',
      color: 'black',
      border: '2px solid blue',
      fontSize: "12px",
      fontWeight: "bold",
      height: '30px',
      margin: '25px 0px 0px 5px'
    }}
        
        
        onClick={refreshBtn}
         type='button'
        ><RefreshIcon fontSize='small'/>refresh</Button></Box>       
    </Box>  
             <Box> 
          
               </Box>
               </Box>
               </Box>  
         {/* Row 2 */}
         <Box
           
           backgroundColor='#F0F8FF'
         
           boxShadow={'5'}
         >
           
         
       <Box
         height="100%"
         width="100%"
       >
         <TableContainer sx={{overflowY: 'auto',height: '70vh', width: '100%'}}>
         <Table stickyHeader aria-label="sticky table" size='small'>
        <TableHead>
          <TableRow>
            {columns.map((headCell) => (
              <TableCell 
                size='small'
                key={headCell.field}
                align={headCell.align}
                style={{ width: headCell.width, minHeight: 10, background: '#233044', color: '#fff', fontFamily: 'sans-serif', fontWeight: 'bold', border: '1px solid white' }}
              >
                {headCell.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
        {loading ? (
                <TableRow>
                  <TableCell colSpan={10} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : filteredRows.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={10} align="center">
                  <Typography>No data found</Typography>
                  </TableCell>
                </TableRow>
              ) :(
          filteredRows.slice(page*rowsPerPage,page*rowsPerPage+rowsPerPage).map((row, index) => (
            <TableRow key={index} style={index % 2 ? { background: "#e3ebf3" } : { background: "#fff" }}>
              {columns.map((column) => (
                <TableCell key={column.field} align={column.align}>
                  {row[column.field]}
                </TableCell>
              ))}
            </TableRow>
          ))
        )}
        </TableBody>
      </Table>

         {/* <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((headCell) => (
                  <TableCell
                    size='small'
                    key={headCell.field}
                    align={headCell.align}
                    sortDirection={orderBy === headCell.field ? order : false}
                   style={{ width: headCell.width,minHeight:10,background: '#7469B6' ,color:'#fff',fontFamily:'sans-serif',fontWeight:'bold',border:'1px solid white' }}   
                  //  sortDirection={orderBy === column.field ? order : false}
                  >
                    <TableSortLabel
                      active={orderBy === headCell.field}
                      direction={orderBy === headCell.field ? order : 'asc'}
                      onClick={() => handleSortRequest(headCell.field)}
                    >
                      {headCell.label}
                    </TableSortLabel>
                  </TableCell>
                ))}
                {/* <TableCell>Action</TableCell> 
              </TableRow>
            </TableHead>
            <TableBody>
              {stableSort(filteredRows, getComparator(order, orderBy))
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row, index) => (
                  <TableRow key={index} style ={ index % 2? { background : "#c6c8dc" }:{ background : "#fff" }}>
                    {columns.map((column) => (
                      <TableCell key={column.field} align={column.align}>
                        {row[column.field]}
                      </TableCell>
                    ))}
                     <TableCell>
                      <IconButton color="primary" onClick={handleDownload(row.id)}>
                        <DownloadIcon />
                      </IconButton>
                    </TableCell> 
                  </TableRow>
                ))}
            </TableBody>
          </Table> */}
         {/* <Table stickyHeader aria-label="sticky table">
           <TableHead >
             <TableRow   >
               {columns.map((column) => (
                 <TableCell
                   key={column.field}
                   align={'center'}
                   style={{ minWidth: column.minWidth,minHeight:10,background: '#7469B6' ,color:'#fff',fontFamily:'sans-serif',fontWeight:'bold',border:'1px solid white' }}   
                   sortDirection={orderBy === column.field ? order : false}
                >
                  <TableSortLabel
                       active={orderBy === column.field}
                       direction={orderBy === column.field ? order : 'asc'}
                       onClick={() => { handleSortRequest(column.field) }}>
                               {column.label}     
                  </TableSortLabel>
                   
                 </TableCell>
               ))}
             </TableRow>
           </TableHead>
           <TableBody >
           {stableSort(filteredRows, getComparator(order, orderBy))
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row, index) => (
                  <TableRow key={index}>
                    {columns.map((column) => (
                      <TableCell key={column.field} align={column.align}>
                        {row[column.field]}
                      </TableCell>
                    ))}
                    {/* <TableCell>
                      <IconButton color="primary" onClick={handleDownload(row.id)}>
                        <DownloadIcon />
                      </IconButton>
                    </TableCell> 
                  </TableRow>
                ))}
           </TableBody>
         </Table> */}
       </TableContainer>
       <TablePagination
                    rowsPerPageOptions={[25,50,100,150]}
                    // rowsPerPage={rowsPerPage}
                    // page={page}
                    // count={filteredRows.length}
                    // component="div"
                    // onPageChange={handlechangepage}
                    // onRowsPerPageChange={handleRowsPerPage}
                    component="div"
                    count={filteredRows.length}
                    page={page}
                    onPageChange={handlechangepage}
                    rowsPerPage={rowsPerPage}
                    onRowsPerPageChange={handleRowsPerPage}
                >

                </TablePagination>
 
       </Box>
     </Box>
    
 
     {/* Row 3 */}
     
           </>
  );
}
