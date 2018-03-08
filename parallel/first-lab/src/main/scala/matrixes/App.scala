package matrixes

// Akka imports
import akka.actor._
import akka.io.{ IO, Tcp }
import akka.util.ByteString

//Scala imports
import scala.concurrent.duration._

//Java imports
import java.net.InetSocketAddress

class Daemon extends Actor {

  import Tcp._
  import context.system

  IO(Tcp) ! Bind(self, new InetSocketAddress("localhost", 8000))

  def receive = {

    case CommandFailed(_: Bind) => context stop self
      
    case c @ Connected(remote, local) =>
      val handler = context.actorOf(Props[SimplisticHandler])
      val connection = sender()
      connection ! Register(handler)
  }

}

class Server extends Actor {

  def receive = {
    case _ => sender() ! "server"
  }

}

class SimplisticHandler extends Actor {
  import Tcp._
  def receive = {
    case Received(data) =>
      val str = data.utf8String.trim
      str match {
        case "hello" => sender() ! Write(ByteString("haii\n"))
        case _       => sender() ! Write(ByteString("unknown command\n"))
      }
    case PeerClosed     => context stop self
  }
}

class Supervisor extends Actor {

  def receive = {
    case _ => sender() ! "supervisor"
  }

}

class Worker extends Actor {

  def receive = {
    case _ => sender() ! "worker"
  }

}

object App {
  def main(args : Array[String]) {

    val system = ActorSystem("daemon-system")

    val daemon = system.actorOf(Props[Daemon], "daemon")

    println( "WATASHI WA NEKO NANODESU SAMPAIIIIIIII" )
  }
}
