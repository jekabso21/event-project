import InfoIcon from '@mui/icons-material/Info';
import WarningIcon from '@mui/icons-material/Warning';
import ReportIcon from '@mui/icons-material/Report';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import * as React from 'react';
import Box from '@mui/joy/Box';
import Alert from '@mui/joy/Alert';
import IconButton from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
export default function Alerts({ status, text }) {
    const [show, setShow] = React.useState(true)

  const statusFormatted = status.charAt(0).toUpperCase() + status.slice(1);

  const items = {
    'success': { color: 'success', icon: <CheckCircleIcon /> },
    'warning': { color: 'warning', icon: <WarningIcon /> },
    'error': { color: 'danger', icon: <ReportIcon /> },
    'neutral': { color: 'neutral', icon: <InfoIcon /> },
  };

    // upon render, starts a 2 seconds countdown to hide the Alert.
    React.useEffect(() => {
    setShow(true); // reset the show status when status or text changes
    const timer = setTimeout(() => {
      setShow(false);
    }, 4000);
    return () => clearTimeout(timer);
  }, [status, text]); // observe status and text

  if (!show) {
    return null;
  }

    return (
        <Box sx={{ display: 'flex', gap: 2, width: '100%', flexDirection: 'column' }}>
            <Alert
                key={statusFormatted}
                sx={{ alignItems: 'flex-start' }}
                startDecorator={items[status].icon}
                variant="soft"
                color={items[status].color}
                endDecorator={
                    <IconButton variant="soft" color={items[status].color}>

                    </IconButton>
                }
            >
                <div>
                    <div>{statusFormatted}</div>
                    <Typography level="body-sm" color={items[status].color}>
                        {text}
                    </Typography>
                </div>
            </Alert>
        </Box>
    );
}