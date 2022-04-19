import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import CourseDetail from "./course-detail";
import { Assignment } from "../api/client";


const rows = [] as Assignment[];

function AssignmentList() {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell align="right">State</TableCell>
            <TableCell align="right">Info</TableCell>
            <TableCell align="right">EndAt</TableCell>
            <TableCell align="right">CreatedAt</TableCell>
            <TableCell align="right">Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((asm) => (
            <TableRow
              key={asm.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {asm.title}
              </TableCell>
              <TableCell align="right">{asm.state}</TableCell>
              <TableCell align="right">{asm.info}</TableCell>
              <TableCell align="right">{asm.end_at}</TableCell>
              <TableCell align="right">{asm.created_at}</TableCell>
              <TableCell align="right">
                {asm.course
                  ? <CourseDetail data={asm.course} />
                  : <p>No Course</p>
                }
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}


export default AssignmentList;
