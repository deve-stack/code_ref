import LandingPage from "../Pages/Public/LandingPage";
import Login from "../Pages/Public/Login";
import Register from "../Pages/Public/Register";
import Root from "../Pages/Hoc/Root";
import SendOtp from "../Pages/Public/SendOtp";
import ForgetPassword from "../Pages/Public/ForgetPassword";
import RootDashboard from "../Pages/Protected/Dashboard/RootDashboard";
import Auth from "../Components/Body/useAuth";
import Profile from "../Pages/Protected/UserProfile/Profile";
import UpcomingEvents from "../Pages/Public/UpcomingEvents";
import Venues from "../Pages/Public/Venues";
import Artists from "../Pages/Public/Artists";
import ChangePassword from "../Pages/Protected/ChangePassword";
import ArtistsList from "../Pages/Protected/Artists/ArtistsList";
import VenuesList from "../Pages/Protected/Venues/VenuesList";
import UpcomeEvents from "../Pages/Protected/Dashboard/upcomeEvent";
import ArtistDetails from "../Pages/Protected/Artists/ArtistDetails";
import ArtistDetailsPublic from "../Pages/Public/ArtistDetailsPublic";
import VenueDetailsPublic from "../Pages/Public/VenueDetailsPublic";
import VenueDetailsPrivate from "../Pages/Protected/Venues/VenueDetailsPrivate";
import MyGigs from "../Pages/Protected/Gigs/MyGigs";
import MyBids from "../Pages/Protected/BidsForVenueManger/Mybids";
import EventDetailsPublic from "../Pages/Public/EventDetailsPublic";

const routes = [
  {
    path: "/",
    element: <Root />,
    children: [
      {
        index: true,
        element: <LandingPage />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/register",
        element: <Register /> ,
      },
      {
        path: "/forget_password",
        element: <SendOtp />, 
      },
      {
        path: "/reset_password",
        element: <ForgetPassword />,
      },
      {
        path: "/upcoming_events",
        element: <UpcomingEvents />,
      },
      {
        path:'/venues',
        element: <Venues/>
      },
      {
        path:'/artist',
        element: <Artists/>
      },
      {
        path: "/artist-detail/:id",
        element: <ArtistDetailsPublic/>,
      },
      {
        path: "/venue-detail/:id",
        element: <VenueDetailsPublic/>,
      },
      {
        path: "event-details/:id",
        element: <EventDetailsPublic/>,
      },
      {
        path: "/bod",
        element: (
          <Auth>
            <RootDashboard />
          </Auth>
        ),
        children: [
          {
            path:'events',
            element: <UpcomeEvents />,
          },
          {
            path: "profile",
            element: <Profile />,
          },
          {
            path: "change_password",
            element: <ChangePassword />,
          },
          {
            path: "artists_list",
            element: <ArtistsList/>,
          },
          {
            path: "venues_list",
            element: <VenuesList/>,
          },
          {
            path: "venue-details/:id",
            element: <VenueDetailsPrivate/>,
          },
          {
            path: "artist-details/:id",
            element: <ArtistDetails/>,
          },
          {
            path: "gigs",
            element: <MyGigs/>,
          },
          {
            path: "bids",
            element: <MyBids/>,
          },
          
        ],
      },
    ],
  },
];

export default routes;