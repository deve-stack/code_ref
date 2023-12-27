import React from 'react'
import moment from "moment";
import DummyImage from "../../../Assets/noimg.jpg";
const OngoingStaus = ({data ,openConfirmationPopup }) => {
  

  const ActionHandler=(btntype)=>{
      openConfirmationPopup(data.id ,data.venue.id ,data.artist.id ,btntype)
    
  }

  return (
    <>
       <div className="col-md-4 mb-2">
      <div className="pb-4 gig-profile-card">
        <div className="">
          <img
            src={data?.artist?.image ? data.artist.image : DummyImage}
            className="mygig-full-image"
          />
        </div>
        <div className="text-end pe-4">
          <img
            src={data?.venue?.image ? data.venue.image : DummyImage}
            className="mygig-rounded-image"
          />
        </div>
        <div className="d-flex align-items-baseline justify-content-center">
          <ul className="list-group">
            <li className=" d-flex   align-items-center">Artist name</li>
            <li className="m d-flex  align-items-center">Start date</li>
            <li className=" d-flex   align-items-center">End date</li>
            <li className="d-flex  align-items-center">offered price</li>
            <li className="d-flex  align-items-center">Asked price</li>
            <li className="d-flex  align-items-center">status</li>
          </ul>
          <ul className="list-group">
            <li className=" d-flex   align-items-center">
              <span className="gig-cards-para">
                {data?.artist?.name ? data.artist.name : "NA"}
              </span>
            </li>
            <li className="m d-flex  align-items-center">
              <span className="gig-cards-para">
                {moment(data?.start_time).format("MMMM Do YYYY, h a")}
              </span>
            </li>
            <li className=" d-flex   align-items-center">
              <span className="gig-cards-para">
                {moment(data?.end_time).format("MMMM Do YYYY, h a")}
              </span>
            </li>

               <li className="d-flex  align-items-center">
              <span className="gig-cards-para">
                {data?.venue_bidding_amount ?data?.venue_bidding_amount: "NA"}
              </span>
            </li>
            <li className="d-flex  align-items-center">
              <span className="gig-cards-para">
                {data?.artist_band_bidding_amount ? data?.artist_band_bidding_amount: "NA"}
              </span>
            </li>
            <li className="d-flex  align-items-center">
              <span className="gig-cards-para text-primary fw-bold ">Ongoing             
              </span>
            </li>
          </ul>
        </div>
        <div className="pt-3 text-center">
        <button onClick={()=>ActionHandler("Accept")}  className="gig-card-btn green" type="btn">Accept
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-check-lg" viewBox="0 0 16 16">
          <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z"/>
        </svg>
        </button>
        <button  onClick={()=>ActionHandler("Reject")} className="gig-card-btn bg-danger" type="btn">Reject
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-x" viewBox="0 0 16 16">
          <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
        </svg>
        </button>
       
      </div>
      </div>
    </div> 
    </>
  )
}

export default OngoingStaus
