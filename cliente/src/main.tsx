import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";
import Home from './views/Home'
import Scaffold from './components/Scaffold'
import TopBar from './components/TopBar'
import BottomBar from './components/BottomBar'
const router = createBrowserRouter([
  {
    path: "/",
    element: <Scaffold TopBar={<TopBar/>} BottomBar={<BottomBar/>}/>,
    children: [
      {path: "", Component: Home}
      ]
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
<RouterProvider router={router} />
  </StrictMode>,
)
