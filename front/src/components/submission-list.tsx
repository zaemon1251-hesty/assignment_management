import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { ReactElement } from "react";

import { Submission } from "../api/client";
import AssignmentDetail from './assignment-detail';

const rows = [] as Submission[];


function SubmissionList():ReactElement {
  return (
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="right">State</TableCell>
              <TableCell align="right">CreatedAt</TableCell>
              <TableCell align="right">Assignment</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((sub) => (
              <TableRow
                key={sub.id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell align="right">{sub.state}</TableCell>
                <TableCell align="right">{sub.created_at}</TableCell>
                <TableCell align="right">
                  {sub.assignment
                    ? <AssignmentDetail data={sub.assignment} />
                    : <p>No Course</p>
                  }
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
  )
}

export default SubmissionList;
