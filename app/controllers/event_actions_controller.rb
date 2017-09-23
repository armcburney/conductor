# frozen_string_literal: true

class EventActionsController < ApplicationController
  before_action :set_event_action, only: %i(show edit update destroy)
  before_action :authenticate_user!

  # GET /event_actions
  # GET /event_actions.json
  def index
    @event_actions = EventAction.all
  end

  # GET /event_actions/1
  # GET /event_actions/1.json
  def show
  end

  # GET /event_actions/new
  def new
    @event_action = EventAction.new
  end

  # GET /event_actions/1/edit
  def edit
  end

  # POST /event_actions
  # POST /event_actions.json
  def create
    @event_action = EventAction.new(event_action_params)

    respond_to do |format|
      if @event_action.save
        format.html { redirect_to @event_action, notice: "Event action was successfully created." }
        format.json { render :show, status: :created, location: @event_action }
      else
        format.html { render :new }
        format.json { render json: @event_action.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /event_actions/1
  # PATCH/PUT /event_actions/1.json
  def update
    respond_to do |format|
      if @event_action.update(event_action_params)
        format.html { redirect_to @event_action, notice: "Event action was successfully updated." }
        format.json { render :show, status: :ok, location: @event_action }
      else
        format.html { render :edit }
        format.json { render json: @event_action.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /event_actions/1
  # DELETE /event_actions/1.json
  def destroy
    @event_action.destroy
    respond_to do |format|
      format.html { redirect_to event_actions_url, notice: "Event action was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private

  def set_event_action
    @event_action = EventAction.find(params[:id])
  end

  def event_action_params
    params
      .require(:event_action)
      .permit(:event_receiver_id, :job_type, :email_address, :webhook_url, :webhook_body)
      .reject{|_, v| v.blank?}
  end
end
