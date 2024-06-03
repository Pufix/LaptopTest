import { createContext, useEffect, useState } from 'react';
import React,{ useContext } from 'react';

var username = "ceapa";
var password;
var token= 0;
var userRegister;
var passRegister;
var edit = false;




function login (setErrLogin, errLogin,setSes, loggedIn, setLoggedIn, regMsg, setRegMsg){
    return(
        <div>
            <h1>Login</h1>
            <input type="text" placeholder="username" onChange={(e) => username = e.target.value}></input>
            <input type="password" placeholder="password" onChange={(e) => password = e.target.value}></input>
            <button onClick={async () =>{
                try{
                await fetch('https://servicempp-43ldisly2q-lm.a.run.app/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({username: username, password: password}),
                }).then((response) => {
                    if (response.status !== 200){
                        setLoggedIn(false);
                        setErrLogin(true);
                    }else{
                        if (response.status === 200){
                            response.json().then((data) => {
                                token = data.session_key;
                                setLoggedIn(true);
                                setErrLogin(false);
                                setSes(true);
                                //save token to cache
                                localStorage.setItem('token', token);
                            });
                        }
                    }
                })}catch (error){
                    setLoggedIn(false);
                    setErrLogin(true)
                }
            }}>
                Login
            </button>
            {errLogin ? <h1>Failed to login</h1> : <h1></h1>}
            <h1>Register</h1>
            <input type="text" placeholder="username" onChange={(e) => userRegister = e.target.value}></input>
            <input type="password" placeholder="password" onChange={(e) => passRegister = e.target.value}></input>
            <button onClick={async () => {
                try{
                await fetch('https://servicempp-43ldisly2q-lm.a.run.app/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({username: userRegister, password: passRegister}),
                }).then((response) => {
                    if (response.status !== 201){
                        if (response.status === 409){
                            setRegMsg(<h1>Username already exists</h1>);

                        }else{
                        setRegMsg(<h1>Failed to register</h1>);}
                    }else{
                        setRegMsg(<h1>Registered</h1>);
                    }
                })}catch (error){
                }
            }}>Register</button>
            {regMsg}
        </div>
    )
}

function validateToken(setSes, loggedIn, setLoggedIn){
    try{
        fetch ('https://servicempp-43ldisly2q-lm.a.run.app/validate/' + token, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then((response) => {
            if (response.status !== 200){
                setLoggedIn(false);
                setSes(false);

            }else{
                setLoggedIn(true);
                setSes(true);
            }
        });
    }catch (error){
        setLoggedIn(false);
        setSes(false);
    }
}

function editProfile(setCeapa, ceapa, setErrEdit, errEdit){
    return(
        <div>
            <h1>Edit Profile</h1>
            <button onClick={() => {setCeapa(false); edit = false; setErrEdit(false);}}>Close edit</button><br></br>
            <input type="text" placeholder="enter new username" onChange={(e) => username = e.target.value}></input><br></br>
            <input type="password" placeholder="enter new password" onChange={(e) => password = e.target.value}></input><br></br>
            <button onClick={async () => {
                try{
                await fetch('https://servicempp-43ldisly2q-lm.a.run.app/editUser/'+ token, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({username: username, password: password}),
                }).then((response) => {
                    if (response.status !== 200){
                        setErrEdit(true);
                    }else{
                        edit = false;
                        setCeapa(false);
                        setErrEdit(false);

                    }
                })}catch (error){
                    setErrEdit(true);
                }
            }}>Edit</button>
        </div>
    )           
}
function kids(children){
    return(
        <div>{children}</div>
    )
}
function exterior(children, setSes, loggedIn, setLoggedIn, setCeapa, ceapa, setErrEdit, errEdit){    
    
    return(
        <div>
            <button onClick={() => {setLoggedIn(false); setSes(false);token = 0;
                                localStorage.setItem('token', token);}}>Logout</button>
            <button onClick={() => {setCeapa(true);edit = true;setCeapa(true);}}>Edit Profile</button>
            {ceapa ? editProfile(setCeapa, ceapa, setErrEdit, errEdit):kids(children) }
        </div>  
    )
}
export function UserContext({children}){
    const [loggedIn, setLoggedIn] = useState(false);
    const [errLogin, setErrLogin] = useState(false);
    const [ses, setSes] = useState(false);
    const [regMsg, setRegMsg] = useState();
    const [ceapa, setCeapa] = useState(false);
    const [plm, setPlm] = useState(false);
    const [errEdit, setErrEdit] = useState();
    //get token from cache
    token = localStorage.getItem('token');
    if (token !== null){
        try{
        validateToken(setSes, loggedIn, setLoggedIn);
        }catch (error){}
    }
    return(
        <div>
            {loggedIn ? exterior(children, setSes, loggedIn, setLoggedIn, setPlm, plm, setErrEdit, errEdit) : login(setErrLogin, errLogin, setSes, loggedIn, setLoggedIn, regMsg, setRegMsg)} 
        </div>
    )
}