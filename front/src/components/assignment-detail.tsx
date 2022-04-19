/* eslint-disable camelcase */

import { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { Assignment } from '../api/client';
import { ASSIGNMENT_STATE_NAME } from '../constants';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

interface dummyProps {
  data: Assignment
}

function AssignmentDetail(props: dummyProps) {
    const [open, setOpen] = useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);
    const { data } = props;
    const { title, state, end_at } = data;
    return (
        <>
          <Button onClick={handleOpen}>Open Asm</Button>
          <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
          >
            <Box sx={style}>
              <Typography id="modal-modal-title" variant="h6" component="h2">
                {title}
              </Typography>
              <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                {state ? ASSIGNMENT_STATE_NAME[state] : ''} <br />
                {end_at}
              </Typography>
            </Box>
          </Modal>
        </>
    );
};
export default AssignmentDetail;
