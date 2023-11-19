import React, { useState, useEffect } from 'react';
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import axios from "axios";
function createData(name, email, date, isAttended) {
  return { name, email, date, isAttended };
}
let newData = [];
const rows = [
  createData("John Doe", "johndoe@gmail.com", "14/8/2025", true),

];

export default function BasicTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
      axios.get('http://127.0.0.1:3800/users/get/allusers')
          .then(response => {
              const users = response.data;
              if (users && Array.isArray(users) && users.length > 0) {
                  users.forEach(user => {
                      const userData = createData(user.name, user.email, user.date, user.scanned);
                      newData.push(userData);
                  });
                  setData(newData);
              }
          })
          .catch(error => {
              console.error("There was an issue fetching users: ", error);
          })
  }, []);
  return (
    <TableContainer component={Paper}>
      <Table
        sx={{
          minWidth: 650,
          "& .MuiTableRow-root:hover": {
            backgroundColor: "#F6F6F6",
            whiteSpace: "nowrap"

          },
        }}
        aria-label="simple table"
      >
        <TableHead>
          <TableRow sx={{ backgroundColor: "#F6F6F6" }}>
            <TableCell sx={{ fontWeight: "600" }}>Name:</TableCell>
            <TableCell sx={{ fontWeight: "600" }}>Email:</TableCell>
            <TableCell sx={{ fontWeight: "600" }}>Register date:</TableCell>
            <TableCell sx={{ fontWeight: "600" }}>Status:</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {newData.map((row) => (
            <TableRow
              key={row.email}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" scope="row">{row.name}</TableCell>
              <TableCell>{row.email}</TableCell>
              <TableCell>{row.date}</TableCell>
              <TableCell sx={{color: row.isAttended? "#36A2EB" : "#FF6384"}}>{row.isAttended? "Attended" : "Not Attend"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}