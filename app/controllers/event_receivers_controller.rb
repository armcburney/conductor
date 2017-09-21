# frozen_string_literal: true

class EventReceiversController < ApplicationController
  before_action :set_event_receiver, only: %i(show edit update destroy)

  # GET /event_receivers
  # GET /event_receivers.json
  def index
    @event_receivers = EventReceiver.all
  end

  # GET /event_receivers/1
  # GET /event_receivers/1.json
  def show
  end

  # GET /event_receivers/new
  def new
    @event_receiver = EventReceiver.new
  end

  # GET /event_receivers/1/edit
  def edit
  end

  # POST /event_receivers
  # POST /event_receivers.json
  def create
    @event_receiver = EventReceiver.new(event_receiver_params)

    respond_to do |format|
      if @event_receiver.save
        format.html { redirect_to @event_receiver, notice: "Event receiver was successfully created." }
        format.json { render :show, status: :created, location: @event_receiver }
      else
        format.html { render :new }
        format.json { render json: @event_receiver.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /event_receivers/1
  # PATCH/PUT /event_receivers/1.json
  def update
    respond_to do |format|
      if @event_receiver.update(event_receiver_params)
        format.html { redirect_to @event_receiver, notice: "Event receiver was successfully updated." }
        format.json { render :show, status: :ok, location: @event_receiver }
      else
        format.html { render :edit }
        format.json { render json: @event_receiver.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /event_receivers/1
  # DELETE /event_receivers/1.json
  def destroy
    @event_receiver.destroy
    respond_to do |format|
      format.html { redirect_to event_receivers_url, notice: "Event receiver was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private

  def set_event_receiver
    @event_receiver = EventReceiver.find(params[:id])
  end

  def event_receiver_params
    params
      .require(:event_receiver)
      .permit(:start_time, :interval, :job_type_id, :action)
  end
end
