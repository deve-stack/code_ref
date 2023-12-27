import React from "react";
import moment from "moment";
import DummyImage from "../../../Assets/noimg.jpg";
import { useSelector } from "react-redux";

const IndivualStatus = ({ data }) => {
  const profile = useSelector((state) => state.Auth.profile);

  return (
    <div className="col-lg-4 col-md-6 mb-2">
      <div className="pb-4 gig-profile-card">
        <div className="">
          {profile.venue_owner == true ? (
            <img
              src={data.artist.image ? data.artist.image : DummyImage}
              className="mygig-full-image"
            />
          ) : (
            <img
              src={data.venue.image ? data.venue.image : DummyImage}
              className="mygig-full-image"
            />
          )}
        </div>
        <div className="text-end pe-4">
          {profile.venue_owner == true ? (
            <img
              src={data.venue.image ? data.venue.image : DummyImage}
              className="mygig-rounded-image"
            />
          ) : (
            <img
              src={data.artist.image ? data.artist.image : DummyImage}
              className="mygig-rounded-image"
            />
          )}
        </div>
        <div className="d-flex align-items-baseline justify-content-center">
          <ul className="list-group">
            <li className=" d-flex   align-items-center">
              {" "}
              {profile.venue_owner == true ? "Artist Name" : "Venue Name"}
            </li>
            <li className="m d-flex  align-items-center">
              {data.status == "Reject" ? "Event date" : " Start date"}
            </li>
            {data.status != "Reject" && (
              <li className=" d-flex   align-items-center">End date</li>
            )}
            {data.status != "Reject" && (
              <li className="d-flex  align-items-center">
                {profile.venue_owner ? "My offer" : "Venue offer"}
              </li>
            )}
            {data.status != "Reject" && (
              <li className="d-flex  align-items-center">
                {" "}
                {profile.venue_owner ? "Artist Offer" : "My offer"}
              </li>
            )}
            {data.status == "Accepted" && (
              <li className="d-flex  align-items-center fw-bold">
                Final gig price
              </li>
            )}
            <li className="d-flex  align-items-center">Status</li>
          </ul>
          <ul className="list-group">
            <li className=" d-flex   align-items-center">
              <span className="gig-cards-para">
                {profile.venue_owner ? data.artist.name : data.venue.name}
              </span>
            </li>
            <li className="m d-flex  align-items-center">
              <span className="gig-cards-para">
                {moment(data?.start_time).format("MMMM Do YYYY, h a")}
              </span>
            </li>
            {data.status != "Reject" && (
              <li className=" d-flex   align-items-center">
                <span className="gig-cards-para">
                  {moment(data?.end_time).format("MMMM Do YYYY, h a")}
                </span>
              </li>
            )}

            {data.status != "Reject" && (
              <li className="d-flex  align-items-center">
                <span className="gig-cards-para">
                  {data?.venue_bidding_amount ? (
                    data.venue_bidding_amount
                  ) : (
                    <span className=""> {data.status=="Accepted" ? "Accepted Artist offer" :"NA"} </span>
                  )}
                </span>
              </li>
            )}
            {data.status != "Reject" && (
              <li className="d-flex  align-items-center">
                <span className="gig-cards-para">
                  {data?.artist_band_bidding_amount ? (
                    data.artist_band_bidding_amount
                  ) : (
                    <span className="  ">Accepted Venue offer </span>
                  )}
                </span>
              </li>
            )}
            {data.status == "Accepted" && (
              <li className="d-flex  align-items-center">
                <span className="gig-cards-para">
                  {data?.artist_band_bidding_amount > data.venue_bidding_amount
                    ? data.artist_band_bidding_amount
                    : data.venue_bidding_amount}
                </span>
              </li>
            )}
            <li className="d-flex  align-items-center ms-4">
              {data.status == "Accepted" && (
                <span className="text-success fw-bold accept-status ">
                  Accepted
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="currentColor"
                    className="bi bi-check-lg mb-1"
                    viewBox="0 0 16 16"
                  >
                    <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z" />
                  </svg>
                </span>
              )}
              {data.status == "Reject" && (
                <span className="text-danger fw-bold reject-status ">
                  Rejected
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="23"
                    height="23"
                    fill="currentColor"
                    className="bi bi-x mb-1"
                    viewBox="0 0 16 16"
                  >
                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                  </svg>
                </span>
              )}
              {data.status == "Pending" && (
                <span className=" fw-bold pending-status ">
                  Pending
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="currentColor"
                    className="bi bi-hourglass-split mb-1"
                    viewBox="0 0 16 16"
                  >
                    <path d="M2.5 15a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11zm2-13v1c0 .537.12 1.045.337 1.5h6.326c.216-.455.337-.963.337-1.5V2h-7zm3 6.35c0 .701-.478 1.236-1.011 1.492A3.5 3.5 0 0 0 4.5 13s.866-1.299 3-1.48V8.35zm1 0v3.17c2.134.181 3 1.48 3 1.48a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 9.052 8.5 8.351z" />
                  </svg>
                </span>
              )}
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default IndivualStatus;
