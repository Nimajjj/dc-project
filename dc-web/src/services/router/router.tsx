import * as React from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import HomeView from "../../views/home_view"


const router = createBrowserRouter([
    {
        path: "/",
        element: <HomeView />,
    },
]);


export default function Router() {
    return (
        <RouterProvider router={router} />
    );
}
