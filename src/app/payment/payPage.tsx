"use client";

import React, { useState, useEffect } from "react";
import { FaCreditCard } from "react-icons/fa";
import Style from "./PayLayout.module.sass";
import ChartComponent from "./chart";
import Paginator from "app/components/shared/Paginator";

interface Payment {
  transaction_date: Date;
  total_transactions: number;
  mongo_id: string;
}

interface PagePayProps {
  data?: any;
  userSecondaryId?: string;
}

export default function PayPage(props: PagePayProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const paymentsPerPage = 10;

  let userPayments = props.data;

  const startIndex = (currentPage - 1) * paymentsPerPage;
  const endIndex = startIndex + paymentsPerPage;
  const currentPayments = userPayments?.slice(startIndex, endIndex);

  const handlePageChange = (pageNumber: number) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className={Style.payLayout__content}>
      <div>
        <ul className={Style.payLayout__list}>
          {currentPayments?.map((payment: any, index: number) => (
            <li className={Style.payLayout__chip} key={index.toString()}>
              <div className={Style.payLayout__content_batch}>
                <strong>Site: {payment.country}</strong>
                <span className={Style.divider} />
                <span>
                  <FaCreditCard /> Payment Type: {payment.payment_method}{" "}
                </span>
                <span className={Style.divider} />
                <span>${payment.total_amount}</span>
              </div>
            </li>
          ))}
        </ul>
        <Paginator
          totalItems={userPayments?.length || 0}
          currentPage={currentPage}
          onPageChange={handlePageChange}
        />
      </div>
      <div className={Style.contentChart}>
        <ChartComponent data={currentPayments || []} />{" "}
        {/* Pasa los datos correspondientes a la página actual */}
      </div>
    </div>
  );
}
