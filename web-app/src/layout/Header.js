import React from 'react';
import { Layout } from 'antd';
import Button from '@mui/material/Button';
import {Link} from "@mui/material";

const { Header: AntdHeader } = Layout;

const Header = (props) => {
  const {} = props;

  return (
    <AntdHeader className="frame-nav">
      <div className="nav-logo">
          <Link
              variant="button"
              color="inherit"
              href="/"
              sx={{ my: 1, mx: 1.5 }}
              style={{textDecoration:'none'}}
          >
              Food For All
          </Link>
      </div>
        <Button className='login-btn' href="/login" variant="outlined" sx={{ my: 1, mx: 1.5 }}>
            Login
        </Button>
    </AntdHeader>
  );
};

export default Header;
