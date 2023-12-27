import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { GetMyBidsAction } from "../../../Redux/Action/Bidding";
import { data } from "../../../Utilities";
import Accepted from "./AcceptTabComponent";
import AcceptedTabComponent from "./AcceptTabComponent";
import RejectedTabComponent from "./RejctedTabComponent";
import PendingTabComponent from "./PendingTabComponent";
import OnGointTabComponent from "./OngoingTabComponent";

const Mybids = () => {
  const dispatch = useDispatch();
  const authToken = useSelector((state) => state.Auth.authToken);
  
  const myBids = useSelector((state) => state.Bids.allBids);
  

  const callMyBidsAction=()=>{
    dispatch(GetMyBidsAction(authToken));
  }
  useEffect(() => {
    callMyBidsAction()
  }, []);

  return (
    <section className="header-tabs mt-5">
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <div className="tabs-section position-relative">
              <nav className="headr-navs-bg">
                <div className="nav nav-tabs" id="nav-tab" role="tablist">
                  <button
                    className="nav-link active"
                    id="Accepted-tabs"
                    data-bs-toggle="tab"
                    data-bs-target="#nav-accept"
                    type="button"
                    role="tab"
                    aria-controls="nav-Accept"
                    aria-selected="true"
                  >
                    Accepted Bids
                  </button>
                  <button
                    className="nav-link"
                    id="Rejected-tabs"
                    data-bs-toggle="tab"
                    data-bs-target="#nav-reject"
                    type="button"
                    role="tab"
                    aria-controls="nav-reject"
                    aria-selected="false"
                  >
                    Rejected Bids
                  </button>
                  <button
                    className="nav-link"
                    id="Ongoing-tabs"
                    data-bs-toggle="tab"
                    data-bs-target="#nav-ongoing"
                    type="button"
                    role="tab"
                    aria-controls="nav-ongoing"
                    aria-selected="false"
                  >
                    Ongoing Bids
                  </button>
                  <button
                    className="nav-link"
                    id="Pening-tabs"
                    data-bs-toggle="tab"
                    data-bs-target="#nav-pending"
                    type="button"
                    role="tab"
                    aria-controls="nav-pending"
                    aria-selected="false"
                  >
                    Pending Bids
                  </button>
                </div>
              </nav>
              <div className="tab-content" id="nav-tabContent">
                <div
                  className="tab-pane fade show active"
                  id="nav-accept"
                  role="tabpanel"
                  aria-labelledby="Accept-tabs"
                >
                  <AcceptedTabComponent data={myBids} />
                </div>
                <div
                  className="tab-pane fade"
                  id="nav-reject"
                  role="tabpanel"
                  aria-labelledby="Rejected-tabs"
                >
                  <RejectedTabComponent data={myBids} />
                </div>
                <div
                  className="tab-pane fade"
                  id="nav-ongoing"
                  role="tabpanel"
                  aria-labelledby="Ongoing-tabs"
                >
                 <OnGointTabComponent callMyBidsAction={callMyBidsAction} data={myBids}/> 
                </div>
                <div
                  className="tab-pane fade"
                  id="nav-pending"
                  role="tabpanel"
                  aria-labelledby="Pending-tabs"
                >
                  <PendingTabComponent data={myBids} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Mybids;
