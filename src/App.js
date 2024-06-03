import logo from './logo.svg';
import './App.css';
import React from 'react';
import ReactDOM, { createPortal } from 'react-dom';
import { createRoot } from 'react-dom';
import Laptop from './classes/laptop';
import Display from './pages/display';
import {Link} from 'react-router-dom';
import { useState } from 'react';
import { Routes, Route, browserRouter } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import AddItemPage from './pages/addItemPage';
import { useContext } from 'react';
import {useNavigate} from 'react-router-dom';
import { createContext } from 'react';

import { LaptopContext, LaptopProvider } from './contexts/laptopcontext';
import EditItemPage from './pages/editItemPage';
import {UserContext} from './contexts/usercontext';

function App() {
	return (
		<div>
			<UserContext>
				<LaptopProvider>
					<BrowserRouter>
						<Routes>
							<Route path="/" element={<Display  />} />
							<Route path="/index" element={<Display  />} />
							<Route path="/addItemPage" element={<AddItemPage />} />
							<Route path="/editItemPage" element={<EditItemPage />}/>
							<Route path='/LaptopShopV2' element={<Display />} >
								<Route path='/LaptopShopV2/addItemPage' element={<AddItemPage />} />
								<Route path='/LaptopShopV2/editItemPage' element={<EditItemPage />} />
							</Route>
						</Routes>
					</BrowserRouter>
				</LaptopProvider>
			</UserContext>
		</div>
	);


}

export default App;
