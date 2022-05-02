import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { ReactElement } from "react";

import { Course } from "../api/client";

const rows = [] as Course[];


function CourseList():ReactElement {
  return (
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="right">Title</TableCell>
              <TableCell align="right">State</TableCell>
              <TableCell align="right">CreatedAt</TableCell>
              <TableCell align="right">UpdatedAt</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((course) => (
              <TableRow
                key={course.id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell align="right">{course.title}</TableCell>
                <TableCell align="right">{course.url}</TableCell>
                <TableCell align="right">{course.created_at}</TableCell>
                <TableCell align="right">{course.updated_at}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
  )
}

export default CourseList;
