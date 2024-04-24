import 'bootstrap/dist/css/bootstrap.min.css';
import { Link, BrowserRouter, Routes, Route } from "react-router-dom";
import axios from 'axios';

import './App.css'
import Login from './components/Login.jsx'
import Profile from './components/Profile.jsx'
import {RequireToken} from './components/Auth.jsx'
import SimpleNav from './components/Nav.jsx'
import SimpleCard from './components/Item.jsx'
import ListItems from './components/ListItems.jsx'


function App() {

  return (
    <>
{/*         <div className="vh-100 gradient-custom"> */}
        <div>
            <div className="container">
                <BrowserRouter>
                    <SimpleNav/>
                        <div>
                            <div className="mask d-flex align-items-center h-100 gradient-custom-3 mt-3">
                                <div className="container h-100">
                                    <div className="row d-flex justify-content-center align-items-center h-100">
                                        <div className="col-12 col-md-9 col-lg-7 col-xl-6">
                                            <Routes>
                                                <Route path='/' element={<Login />}/>
                                                <Route path='/profile' element={
                                                    <RequireToken>
                                                        <Profile />
                                                    </RequireToken>
                                                    }
                                                />
                                                <Route path='/items' element={
                                                    <RequireToken>
                                                        <ListItems />
                                                    </RequireToken>
                                                    }
                                                />
                                            </Routes>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                </BrowserRouter>
            </div>
        </div>
    </>
  )
}

export default App
